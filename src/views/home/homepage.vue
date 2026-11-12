<template>
  <div class="portal-home">
    <header class="portal-header">
      <div class="portal-wrap portal-header-inner">
        <router-link class="portal-brand" to="/">Iso-Seq DB</router-link>
        <nav aria-label="Main navigation">
          <router-link to="/dashboard">Database</router-link>
          <router-link to="/about/about">About</router-link>
        </nav>
      </div>
    </header>

    <main>
      <section class="portal-hero" data-enter>
        <div class="portal-wrap portal-banner">
          <h1>Iso-Seq Transcript Database</h1>
          <p>Explore full-length transcripts, compare expression across populations, and browse variant annotations.</p>
          <form class="portal-search" @submit.prevent="quickSearch">
            <label for="portal-transcript">Transcript ID</label>
            <div class="portal-search-controls">
              <el-input id="portal-transcript" v-model="quickKeyword" placeholder="Enter a transcript ID" required />
              <el-button type="primary" native-type="submit">Search transcripts</el-button>
            </div>
          </form>
          <router-link class="portal-example" :to="{ path: transcriptPath, query: { keyword: 'DEMO-TX-11' } }">
            Try DEMO-TX-11 <span aria-hidden="true">→</span>
          </router-link>
        </div>
      </section>

      <section class="portal-wrap portal-directory">
        <h2>Browse the database</h2>
        <div class="portal-grid">
          <router-link v-for="entry in entries" :key="entry.path" :to="entry.path" class="portal-entry">
            <span class="portal-entry-heading">{{ entry.title }} <span aria-hidden="true">↗</span></span>
            <span>{{ entry.description }}</span>
          </router-link>
        </div>
      </section>
    </main>
    <footer class="portal-footer">
      <div class="portal-wrap">Iso-Seq Transcript Database</div>
    </footer>
  </div>
</template>

<script>
const transcriptPath = '/search/information/transcriptSearch'

export default {
  name: 'Home',
  data() {
    return {
      quickKeyword: '',
      transcriptPath,
      entries: [
        { title: 'Transcript annotation', path: transcriptPath, description: 'SQANTI3 categories, detection rates and splice junction support.' },
        { title: 'Population expression', path: '/search/expression/geneSearch', description: 'Gene and transcript TPM, plus transcript usage by population.' },
        { title: 'Differential analysis', path: '/analysis/differential', description: 'Gene expression, transcript expression and usage results.' },
        { title: 'QTL associations', path: '/analysis/qtl', description: 'Expression, isoform and splicing associations.' },
        { title: 'Variant annotation', path: '/variants', description: 'Transcript consequences, coding potential and ClinVar classifications.' },
        { title: 'Transcript structure', path: '/search/structure', description: 'Run SQANTI3 and browse structural analysis outputs.' }
      ]
    }
  },
  methods: {
    quickSearch() {
      const keyword = this.quickKeyword.trim()
      if (keyword) this.$router.push({ path: this.transcriptPath, query: { keyword }})
    }
  }
}
</script>

<style scoped>
.portal-home { background: #f6f8fa; min-height: 100vh; }
.portal-wrap { width: min(1120px, calc(100% - 48px)); margin-inline: auto; }
.portal-header { background: #0b172d; color: #fff; }
.portal-header-inner { display: flex; justify-content: space-between; align-items: center; min-height: 68px; gap: 16px; }
.portal-brand { color: #fff; font-size: 22px; font-weight: 700; white-space: nowrap; }
.portal-header nav { display: flex; gap: clamp(12px, 3vw, 32px); }
.portal-header nav a { display: flex; align-items: center; min-height: 44px; }
.portal-header nav a:hover { color: #ffbd70; }
.portal-hero { padding-top: 24px; }
.portal-banner { background: #10233e; color: #fff; border-radius: 8px; padding: clamp(28px, 7vw, 96px); border-top: 3px solid #e18a34; }
.portal-hero h1 { font-size: clamp(32px, 5vw, 56px); letter-spacing: -.035em; line-height: 1.1; margin: 0 0 18px; }
.portal-hero p { color: #d4e0ed; font-size: 17px; line-height: 1.6; max-width: 620px; margin: 0 0 30px; }
.portal-search { max-width: 620px; }
.portal-search label { display: block; margin-bottom: 8px; font-weight: 600; }
.portal-search-controls { display: flex; gap: 10px; }
.portal-example { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; color: #ffbd70; }
.portal-example:hover { color: #ffbd70; text-decoration: underline; }
.portal-directory { padding-block: 44px 64px; }
.portal-directory h2 { margin: 0 0 20px; font-size: 24px; }
.portal-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.portal-entry { display: flex; flex-direction: column; gap: 8px; padding: 20px; background: #fff; border: 1px solid #dce4ea; border-radius: 6px; color: var(--portal-muted); line-height: 1.5; transition: transform .18s ease, border-color .18s ease; }
.portal-entry:hover { transform: translateY(-2px); border-color: var(--portal-accent); color: var(--portal-muted); }
.portal-entry-heading { display: flex; justify-content: space-between; gap: 12px; color: var(--portal-accent); font-size: 17px; font-weight: 650; }
.portal-footer { border-top: 1px solid #dce4ea; padding: 24px 0; color: var(--portal-muted); }
@media (max-width: 850px) { .portal-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 540px) {
  .portal-wrap { width: calc(100% - 32px); }
  .portal-grid { grid-template-columns: 1fr; }
  .portal-search-controls { flex-direction: column; }
}
@media (prefers-reduced-motion: no-preference) {
  .portal-hero [id], .portal-hero h1 { animation: portal-enter .38s ease-out both; }
  @keyframes portal-enter { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
}
@media (prefers-reduced-motion: reduce) { .portal-entry { transition: none; } }
</style>
