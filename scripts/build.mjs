import { build } from 'astro';
import { copyFile, mkdir, readdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

// Never copy public's template images or empty docs (which already contains images).
// Only the explicitly approved text asset enters the temporary public directory.
const root = new URL('../', import.meta.url);
const textPublic = new URL('../tmp/staging-public/', import.meta.url);
await mkdir(textPublic, { recursive: true });
const entries = await readdir(textPublic);
if (entries.some((name) => name !== '.nojekyll')) {
  throw new Error('Temporary public directory must contain only .nojekyll');
}
await copyFile(new URL('public/.nojekyll', root), new URL('.nojekyll', textPublic));
await build({
  root: fileURLToPath(root),
  publicDir: fileURLToPath(textPublic),
  vite: { build: { emptyOutDir: false } },
});
