// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://betty-roulette.github.io',
  base: '/staging',
  outDir: './docs',
});