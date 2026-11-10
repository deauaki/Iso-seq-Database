<template>
  <div class="app-container">
    <el-alert title="SQANTI3 demo data · Try DEMO-TX-11" type="info" :closable="false" />
    <!-- ⭐ Filter Section -->
    <div class="filter-container">
      <el-form :inline="true" :model="query">

        <!-- Input Field -->
        <el-form-item label="Transcript">
          <el-input v-model="query.transcript" placeholder="transcript ID" />
        </el-form-item>

        <el-form-item label="SQANTI3 category">
          <el-select v-model="query.category" clearable @change="filterTranscript">
            <el-option v-for="category in categories" :key="category" :label="category" :value="category" />
          </el-select>
        </el-form-item>

        <!-- Query and Reset -->
        <div class="button-wrapper">
          <el-button type="primary" @click="filterTranscript">Query Transcript Annotation Information</el-button>
          <el-button @click="resetFilters">Reset</el-button>
        </div>
      </el-form>
    </div>

    <br>

    <!-- Table Display -->
    <el-table
      v-loading="listLoading"
      :data="paginatedList"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column type="expand">
        <template slot-scope="{ row }">
          <div v-if="row.isDemo">
            <p><strong>Synthetic SQANTI3 evidence</strong></p>
            <p v-for="junction in row.junctions" :key="junction.site">
              {{ junction.site }} · {{ junction.supportingSampleCount }} supporting samples
            </p>
            <p v-if="!row.externalMatches.length">No external database matches</p>
            <p v-for="match in row.externalMatches" :key="match.accession">
              {{ match.database }} ({{ match.version }}) · {{ match.accession }}
            </p>
            <router-link :to="{ path: '/search/expression/geneSearch', query: { keyword: row.geneId } }">
              View population expression
            </router-link>
          </div>
          <p v-else>SQANTI3 evidence unavailable</p>
        </template>
      </el-table-column>
      <el-table-column
        v-for="col in columns"
        :key="col.prop"
        :label="col.label"
        :prop="col.prop"
        :width="col.width"
        align="center"
      >
        <template slot-scope="scope">
          {{ scope.row[col.prop] }}
        </template>
      </el-table-column>
      <el-table-column label="SQANTI3 category" prop="structuralCategory" width="155">
        <template slot-scope="{ row }">{{ row.structuralCategory || '—' }}</template>
      </el-table-column>
      <el-table-column label="Sample support" width="130">
        <template slot-scope="{ row }">
          {{ row.isDemo ? row.supportingSampleCount + '/' + row.eligibleSampleCount : '—' }}
        </template>
      </el-table-column>
      <el-table-column label="Detection" width="100">
        <template slot-scope="{ row }">{{ detectionRate(row) }}</template>
      </el-table-column>
    </el-table>

    <!-- Pagination Component -->
    <div class="pagination" style="text-align:center; margin-top:20px;">
      <el-pagination
        background
        layout="total, prev, pager, next, jumper"
        :total="filteredList.length"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="handlePageChange"
      />
    </div>

  </div>
</template>

<script>
import { getDemoTranscripts } from '@/api/demoTranscriptome'
import { getTranscriptInfo } from '@/api/transcriptInfo'

export default {
  data() {
    return {
      list: [],
      filteredList: [], // ⭐ 筛选后的数据
      listLoading: true,
      currentPage: 1, // 当前页码
      pageSize: 10, // 每页显示条数
      query: { transcript: '', category: '' },
      categories: ['FSM', 'ISM', 'NIC', 'NNC'],
      columns: [
        { label: 'TranscriptId', prop: 'transcriptId', width: 300 },
        { label: 'GeneName', prop: 'geneName', width: 250 },
        { label: 'GeneId', prop: 'geneId', width: 250 },
        { label: 'Chromosome', prop: 'chromosome', width: 150 },
        { label: 'Start', prop: 'start', width: 150 },
        { label: 'End', prop: 'end', width: 150 },
        { label: 'Strand', prop: 'strand', width: 150 },
        { label: 'GeneType', prop: 'geneType', width: 200 }
      ]
    }
  },
  computed: {
    // 计算要显示的数据
    paginatedList() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredList.slice(start, end)
    }
  },
  watch: {
    '$route.query.keyword': {
      immediate: true,
      handler(keyword) {
        this.query.transcript = typeof keyword === 'string' ? keyword : ''
        this.filterTranscript()
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getTranscriptInfo().then(response => {
        this.list = [...getDemoTranscripts(), ...response.data.items]
        this.filterTranscript()
        this.listLoading = false
      })
    },
    // ⭐ 分页（在模板的分页组件里绑定该事件）
    handlePageChange(page) {
      this.currentPage = page
    },
    // ⭐ 点击查询
    filterTranscript() {
      const keyword = this.query.transcript.trim().toLowerCase()
      this.filteredList = this.list.filter(item =>
        (!keyword || String(item.transcriptId).toLowerCase() === keyword) &&
        (!this.query.category || item.structuralCategory === this.query.category)
      )
      this.currentPage = 1
    },

    detectionRate(row) {
      return row.eligibleSampleCount ? (100 * row.supportingSampleCount / row.eligibleSampleCount).toFixed(1) + '%' : '—'
    },

    // ⭐ 点击重置
    resetFilters() {
      this.query = { transcript: '', category: '' }
      this.filteredList = this.list
      this.currentPage = 1
    }
  }
}
</script>

<style scoped>
.filter-container {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px; /* 控制间距 */
  background: #f6f6f6;
  padding: 20px 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.filter-container .el-input,
.filter-container .el-select {
  width: 180px;
}

.filter-container .el-button {
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
}

.filter-container .el-button.el-button--primary {
  background-color: #4e73df;
  border-color: #4e73df;
}

.filter-container .el-button.el-button--primary:hover {
  background-color: #3558c2;
  border-color: #3558c2;
}

.filter-container .el-button.el-button--info {
  background-color: #a0aec0;
  border-color: #a0aec0;
}

.filter-container .el-button.el-button--info:hover {
  background-color: #7b8794;
  border-color: #7b8794;
}

.button-wrapper {
  width: 100%;       /* 占满整行 */
  margin: 15px 0;
  justify-content: center;
}

.filtered-container h4 {
  margin: 0;        /* 先清除浏览器默认 margin */
  padding: 0;  /* 自己控制间距 */
}

</style>
