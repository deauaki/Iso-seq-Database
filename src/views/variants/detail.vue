<template>
  <div class="app-container">
    <router-link :to="{ name: 'VariantSearch' }">← Variant search</router-link>
    <h1>{{ $route.params.variantId }}</h1>
    <el-alert title="Synthetic demo · Consequences and ClinVar labels are illustrative" type="info" :closable="false" />
    <template v-if="variant">
      <p>{{ variant.assembly }} · {{ variant.chrom }}:{{ variant.pos }} · {{ variant.ref }} → {{ variant.alt }}</p>
      <router-link :to="{ name: 'QtlAnalysis', query: { keyword: variant.variantId } }">Find QTL associations</router-link>
      <h2>Transcript consequences</h2>
      <el-table :data="variant.transcriptConsequences" border>
        <el-table-column label="Transcript" min-width="140">
          <template slot-scope="{ row }">
            <router-link :to="{ path: '/search/information/transcriptSearch', query: { keyword: row.transcriptId } }">
              {{ row.transcriptId }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column label="MANE status" prop="maneStatus" min-width="125" />
        <el-table-column label="CPC2 potential" prop="cpc2" min-width="135" />
        <el-table-column label="Functional consequence" prop="consequence" min-width="180" />
        <el-table-column label="Affected exon" prop="exon" min-width="115" />
        <el-table-column label="Affected CDS" min-width="115">
          <template slot-scope="{ row }">{{ row.cds || '—' }}</template>
        </el-table-column>
        <el-table-column label="Median TPM" min-width="115">
          <template slot-scope="{ row }">
            <router-link :to="{ path: '/search/expression/geneSearch', query: { keyword: row.geneId } }">
              {{ row.medianTpm }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column label="Detection" min-width="100">
          <template slot-scope="{ row }">{{ (row.detectionRate * 100).toFixed(1) }}%</template>
        </el-table-column>
      </el-table>
      <h2>ClinVar original classification</h2>
      <p v-if="!variant.clinvar.length">No matching ClinVar records</p>
      <ul v-else>
        <li v-for="record in variant.clinvar" :key="record.accession">{{ record.accession }} · {{ record.classification }}</li>
      </ul>
    </template>
    <p v-else-if="!loading">Variant not found</p>
  </div>
</template>

<script>
import { getVariant } from '@/api/demoAssociations'

export default {
  data() {
    return { variant: null, loading: true }
  },
  watch: {
    '$route.params.variantId': {
      immediate: true,
      async handler(id) {
        this.loading = true
        const variant = await getVariant(id)
        if (this.$route.params.variantId !== id) return
        this.variant = variant
        this.loading = false
      }
    }
  }
}
</script>
