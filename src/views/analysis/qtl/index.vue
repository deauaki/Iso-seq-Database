<template>
  <div class="app-container">
    <h1>QTL Associations</h1>
    <el-alert title="Synthetic demo · Associations and genotype groups are illustrative" type="info" :closable="false" />
    <el-tabs v-model="type" @input="search">
      <el-tab-pane v-for="tab in types" :key="tab" :label="tab" :name="tab" />
    </el-tabs>
    <el-form :inline="true" @submit.native.prevent="search">
      <el-form-item label="Gene, transcript or variant ID">
        <el-input v-model="keyword" placeholder="DEMO-VAR-1" clearable @clear="search" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit">Search</el-button>
      </el-form-item>
    </el-form>
    <el-table :data="items" row-key="id" border empty-text="No matching associations">
      <el-table-column type="expand">
        <template slot-scope="{ row }">
          <div v-if="row.fineMapping">
            <p>Credible set: {{ row.fineMapping.credibleSetId }} ({{ row.fineMapping.coverage * 100 }}%)</p>
            <p>Posterior inclusion probability: {{ row.fineMapping.posteriorProbability }}</p>
          </div>
          <p v-else>Fine-mapping results unavailable</p>
          <genotype-plot v-if="row.genotypeGroups.length" :groups="row.genotypeGroups" />
          <p v-else>Genotype group summaries unavailable</p>
        </template>
      </el-table-column>
      <el-table-column label="Variant" min-width="125">
        <template slot-scope="{ row }">
          <router-link :to="{ name: 'VariantDetail', params: { variantId: row.variantId } }">{{ row.variantId }}</router-link>
        </template>
      </el-table-column>
      <el-table-column label="Gene" prop="geneId" min-width="130" />
      <el-table-column label="Transcript" min-width="120">
        <template slot-scope="{ row }">{{ row.transcriptId || '—' }}</template>
      </el-table-column>
      <el-table-column label="Associated phenotype" prop="phenotype" min-width="180" />
      <el-table-column label="Effect / other allele" min-width="155">
        <template slot-scope="{ row }">{{ row.effectAllele }} / {{ row.otherAllele }}</template>
      </el-table-column>
      <el-table-column label="β" prop="beta" width="80" />
      <el-table-column label="P value" prop="pValue" min-width="90" />
      <el-table-column label="Adjusted P" prop="adjustedPValue" min-width="105" />
      <el-table-column label="Significant (FDR 5%)" min-width="155">
        <template slot-scope="{ row }">{{ 0.05 > row.adjustedPValue ? 'Yes' : 'No' }}</template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getQtlAssociations } from '@/api/demoAssociations'
import GenotypePlot from './GenotypePlot.vue'

export default {
  components: { GenotypePlot },
  data() {
    return { types: ['eQTL', 'isoQTL', 'sQTL'], type: 'eQTL', keyword: '', items: [] }
  },
  created() {
    this.keyword = typeof this.$route.query.keyword === 'string' ? this.$route.query.keyword : ''
    this.search()
  },
  methods: {
    async search() {
      this.items = await getQtlAssociations({ type: this.type, keyword: this.keyword })
    }
  }
}
</script>
