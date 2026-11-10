<template>
  <div class="app-container">
    <h1>Differential Analysis</h1>
    <el-alert title="Synthetic demo · Results are illustrative" type="info" :closable="false" />
    <el-tabs v-model="type" @tab-click="applyFilters">
      <el-tab-pane label="DGE" name="DGE" />
      <el-tab-pane label="DTE" name="DTE" />
      <el-tab-pane label="DTU" name="DTU" />
    </el-tabs>
    <el-form :inline="true" @submit.native.prevent="applyFilters">
      <el-form-item label="Contrast">
        <el-select v-model="analysisId" @change="applyFilters">
          <el-option
            v-for="contrast in contrasts"
            :key="contrast.analysisId"
            :value="contrast.analysisId"
            :label="contrast.numerator + ' vs ' + contrast.denominator"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="Gene or transcript ID">
        <el-input v-model="keyword" placeholder="DEMO-GENE-1" clearable @clear="applyFilters" />
      </el-form-item>
      <el-form-item>
        <el-checkbox v-model="significantOnly" @change="applyFilters">Adjusted P &lt; 0.05</el-checkbox>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit">Search</el-button>
      </el-form-item>
    </el-form>
    <p>Effects are expressed as the first population relative to the second.</p>
    <p v-if="type === 'DTU'">Gene rows show the overall usage test. Transcript rows show changes in usage in percentage points.</p>
    <el-alert v-if="error" title="Unable to load results" type="error" :closable="false" />
    <el-table v-loading="loading" :data="items" border empty-text="No matching results">
      <el-table-column label="Gene" min-width="150">
        <template slot-scope="{ row }">
          <router-link :to="{ path: '/search/expression/geneSearch', query: { keyword: row.geneId } }">
            {{ row.geneId }}
          </router-link>
        </template>
      </el-table-column>
      <el-table-column v-if="type !== 'DGE'" key="transcript" label="Transcript" min-width="150">
        <template slot-scope="{ row }">
          <router-link v-if="row.transcriptId" :to="{ path: '/search/information/transcriptSearch', query: { keyword: row.transcriptId } }">
            {{ row.transcriptId }}
          </router-link>
          <span v-else>—</span>
        </template>
      </el-table-column>
      <el-table-column key="testLevel" label="Test level" prop="testLevel" min-width="110" />
      <el-table-column key="effect" :label="type === 'DTU' ? 'Usage change (pp)' : 'Log₂ fold change'" min-width="155">
        <template slot-scope="{ row }">{{ row.effect == null ? '—' : row.effect }}</template>
      </el-table-column>
      <el-table-column label="P value" prop="pValue" sortable min-width="100" />
      <el-table-column label="Adjusted P" prop="adjustedPValue" sortable min-width="120" />
    </el-table>
    <el-pagination
      class="results-pagination"
      layout="total, prev, pager, next"
      :total="total"
      :current-page="page"
      :page-size="pageSize"
      @current-change="changePage"
    />
  </div>
</template>

<script>
import { getDifferentialContrasts, getDifferentialResults } from '@/api/differentialResults'

export default {
  data() {
    const contrasts = getDifferentialContrasts()
    return {
      contrasts,
      analysisId: contrasts[0].analysisId,
      type: 'DGE',
      keyword: '',
      appliedKeyword: '',
      significantOnly: false,
      items: [],
      total: 0,
      page: 1,
      pageSize: 10,
      loading: false,
      error: false,
      requestId: 0
    }
  },
  created() {
    this.loadResults()
  },
  methods: {
    applyFilters() {
      this.appliedKeyword = this.keyword
      this.changePage(1)
    },
    changePage(page) {
      this.page = page
      this.loadResults()
    },
    async loadResults() {
      const requestId = ++this.requestId
      this.loading = true
      this.error = false
      try {
        const { data } = await getDifferentialResults({
          type: this.type,
          analysisId: this.analysisId,
          keyword: this.appliedKeyword,
          significantOnly: this.significantOnly,
          page: this.page,
          pageSize: this.pageSize
        })
        if (requestId !== this.requestId) return
        this.items = data.items
        this.total = data.total
      } catch (error) {
        if (requestId !== this.requestId) return
        this.error = true
        this.items = []
        this.total = 0
      } finally {
        if (requestId === this.requestId) this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.results-pagination {
  margin-top: 16px;
}
</style>
