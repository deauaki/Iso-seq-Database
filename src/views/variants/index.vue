<template>
  <div class="app-container">
    <h1>Variant Annotations</h1>
    <el-alert title="Synthetic demo · Variant annotations are illustrative" type="info" :closable="false" />
    <el-form class="search-form" :inline="true" @submit.native.prevent="search">
      <el-form-item label="Variant ID or chromosome:position">
        <el-input v-model="keyword" placeholder="DEMO-VAR-1" clearable @clear="search" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit">Search</el-button>
      </el-form-item>
    </el-form>
    <el-table :data="items" border empty-text="No matching variants">
      <el-table-column label="Variant" min-width="140">
        <template slot-scope="{ row }">
          <router-link :to="{ name: 'VariantDetail', params: { variantId: row.variantId } }">{{ row.variantId }}</router-link>
        </template>
      </el-table-column>
      <el-table-column label="Assembly" prop="assembly" />
      <el-table-column label="Chromosome" prop="chrom" />
      <el-table-column label="Position" prop="pos" />
      <el-table-column label="REF" prop="ref" />
      <el-table-column label="ALT" prop="alt" />
    </el-table>
  </div>
</template>

<script>
import { getVariants } from '@/api/demoAssociations'

export default {
  data() {
    return { keyword: '', items: [] }
  },
  created() {
    this.search()
  },
  methods: {
    async search() {
      this.items = await getVariants(this.keyword)
    }
  }
}
</script>

<style scoped>
.search-form {
  margin-top: 16px;
}
</style>
