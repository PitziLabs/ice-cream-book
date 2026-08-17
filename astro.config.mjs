import { defineConfig } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
import sitemap from '@astrojs/sitemap';
import { rehypeRecipeSections } from './src/lib/sections.mjs';

export default defineConfig({
  site: 'https://icecreamtofightwith.com',
  integrations: [sitemap()],
  markdown: {
    // Astro 7 defaults Markdown to the Sätteri processor; opt back into the
    // unified (remark/rehype) pipeline via @astrojs/markdown-remark so our
    // rehype plugin keeps running. `unified()` preserves Astro's defaults
    // (GFM + SmartyPants) and appends our plugin. Structure recipe bodies
    // into the editorial section layout. The book's profanity renders
    // uncensored — no redaction pass.
    processor: unified({ rehypePlugins: [rehypeRecipeSections] }),
  },
});
