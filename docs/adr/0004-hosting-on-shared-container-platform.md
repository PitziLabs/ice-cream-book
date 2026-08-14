# ADR-0004: Hosting on the fleet's shared container platform

**Status:** Accepted (2026-05-26; reconstructed 2026-08-13)

## Context

Before 2026-05, the Astro application source and its deploy workflow lived
in `foundry-platform-demo/app/`, and this repo fired a cross-repo
`repository_dispatch` event when recipes changed to trigger a build
elsewhere. Issue solidago#55 (referenced in `docs/INFRASTRUCTURE_RELATIONSHIP.md`)
split that arrangement apart: PR #83 in this repo ("migration: import
Astro app from foundry-platform-demo," merged 2026-05-26) moved the Astro
application source and a new `deploy.yml` into this repo, so the
application lives alongside the content it serves, while the renamed
`solidago` repo owns only infrastructure (ECR, ECS, ALB, IAM trust) via
Terraform.

The resulting shape, current in this repo today: `.github/workflows/deploy.yml`
builds the Astro static site, packages it into an `nginx:latest` container
(`Dockerfile`, port 8080, `/health` endpoint), pushes to ECR repo
`solidago-dev-app`, and rolls out ECS Fargate service `solidago-dev-app` in
cluster `solidago-dev-cluster`, all behind a shared ALB with Route 53 + ACM.
Authentication is OIDC — the workflow assumes IAM role
`solidago-dev-github-actions` (trust policy scoped to
`repo:lentago/site-icecreamtofightwith-com:*`) for short-lived credentials;
no static AWS keys are stored in GitHub Secrets. The repo itself was
renamed from `ice-cream-book` to `site-icecreamtofightwith-com` on
2026-07-04 as part of a fleet-wide `site-<domain>` naming convention
(documented in both this repo's `docs/INFRASTRUCTURE_RELATIONSHIP.md` and
solidago's CLAUDE.md).

Per solidago's own CLAUDE.md, `icecreamtofightwith.com` is that platform's
"primary app," and later platform-hosted sites (`site_lentago`,
`pondviewlane.com`, `essexcrossingatmontserrat.com`) are added as
additional `modules/site` instances riding the same shared ALB, ECS
cluster, and app security group established for this application. Neither
this repo nor the solidago evidence reviewed explicitly frames this repo
as a deliberate "pattern to replicate" for those later sites — that
framing is an inference from the shared infrastructure, not a recorded
statement — so it is noted here as context rather than asserted as fact.

## Decision

Host the built Astro site as a containerized workload (nginx serving the
static build) on the fleet's shared AWS platform — ECR + ECS Fargate
behind an ALB, provisioned and owned by the `solidago` Terraform repo —
authenticated via OIDC from this repo's own `deploy.yml`, rather than
continuing the prior cross-repo dispatch arrangement or moving to a
static-hosting-specific service.

## Alternatives

- **Recorded, previously in place and replaced:** the cross-repo
  `repository_dispatch` arrangement, where the Astro app source and deploy
  workflow lived in `foundry-platform-demo/app/` and this repo only fired
  an event on recipe changes. PR #83 replaced this explicitly, citing "No
  more cross-repo `repository_dispatch`" as a stated benefit of bringing
  the app source into this repo.
- *Retrospective — not considered at the time:* static hosting purpose-
  built for this workload — S3 + CloudFront, or GitHub Pages — instead of
  a full container on ECS Fargate. **Cheaper and simpler for what this
  repo actually serves** (a static Astro build with no server-side
  logic beyond an nginx health check) **but worse as what this repo
  demonstrates.** This repo's own README frames itself as "a real content
  pipeline... run with the same rigor as any production service" and
  explicitly showcases OIDC-authenticated container deploys to ECS
  Fargate as one of the patterns it exists to demonstrate; a static-file
  host would serve the site adequately but would not exercise (or
  showcase) the container build/push/rollout path the fleet's other,
  more complex workloads also depend on. This tradeoff does not appear to
  have been discussed in the sources reviewed — it is assessed here
  retrospectively, not reconstructed from a recorded debate.

## Consequences

- Deploys depend on solidago's Terraform-managed infrastructure staying in
  sync with what `deploy.yml` expects; a rename or resource change on the
  solidago side (as happened with the `foundry-*` → `solidago-*` rename,
  PR #126) breaks this repo's deploy until `deploy.yml`'s `env` block is
  updated to match.
- No static AWS credentials are stored in this repo; every deploy gets
  fresh credentials via OIDC, scoped to this repo by the IAM trust policy.
- This repo's deploy workflow is a template other application repos on
  the same platform can plausibly follow (same ECR/ECS/OIDC shape), though
  no evidence reviewed confirms that borrowing has actually happened for
  any specific later site.
