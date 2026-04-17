<template>
  <div class="sqanti-page">
    <div class="page-header">
      <h1>SQANTI3 Transcript Structure Analysis</h1>
      <p>
        Upload isoform file and automatically run SQANTI3 analysis to visualize transcript structures.
      </p>
    </div>

    <!-- Upload + Run -->
    <div class="card">
      <h2>1. Upload & Run Analysis</h2>
      <p class="desc">
        Supported formats: GTF / GFF / FASTA
      </p>

      <div class="upload-section">
        <input type="file" @change="handleFileChange" />
        <button
          class="primary-btn"
          @click="runSqanti3"
          :disabled="!selectedFile || running"
        >
          {{ running ? 'Running...' : 'Upload & Run' }}
        </button>
      </div>

      <div v-if="selectedFile" class="info-box">
        <strong>Selected file:</strong> {{ selectedFile.name }}
      </div>

      <div v-if="analysisStatus" class="status-box">
        <strong>Status:</strong> {{ analysisStatus }}
      </div>

      <div v-if="errorMessage" class="error-box">
        ❌ {{ errorMessage }}
      </div>
    </div>

    <!-- Result Files -->
    <div class="card">
      <div class="result-header">
        <h2>2. Result Files</h2>
        <button class="secondary-btn" @click="fetchResults">Refresh</button>
      </div>

      <div v-if="results.length === 0" class="empty-box">
        No result files found yet.
      </div>

      <ul v-else class="result-list">
        <li v-for="file in results" :key="file" class="result-item">
          <span>{{ file }}</span>
          <a
            class="download-link"
            :href="`${backendBase}/api/results/${file}`"
            target="_blank"
          >
            Download
          </a>
        </li>
      </ul>
    </div>

    <!-- Visualization -->
    <div class="card" ref="browserSection">
      <h2>3. Visualization</h2>
      <p class="desc">
        Interactive transcript structure visualization (UCSC Genome Browser Hub)
      </p>

      <!-- ✅ 有结果 -->
      <iframe
        v-if="browserUrl"
        :src="browserUrl"
        width="100%"
        height="800px"
        style="border: none; border-radius: 12px;"
      ></iframe>

      <!-- ❌ 没结果 → 占位 -->
      <div v-else class="empty-visual-box">
        <div class="placeholder">
          <div class="icon">❕</div>
          <p>No visualization available yet</p>
          <span>Please upload a file and run analysis</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StructureView',
  data() {
    return {
      backendBase: 'http://127.0.0.1:5001',
      selectedFile: null,
      running: false,
      analysisStatus: '',
      errorMessage: '',
      browserUrl: '',
      results: []
    }
  },

  mounted() {
    this.fetchResults()
  },

  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0] || null
      this.errorMessage = ''
      this.analysisStatus = ''
      this.browserUrl = ''
    },

    async runSqanti3() {
      if (!this.selectedFile) return

      this.running = true
      this.analysisStatus = 'Running SQANTI3 analysis...'
      this.errorMessage = ''
      this.browserUrl = ''

      const formData = new FormData()
      formData.append('file', this.selectedFile)

      try {
        const response = await fetch(`${this.backendBase}/api/run-sqanti3`, {
          method: 'POST',
          body: formData
        })

        const data = await response.json()

        if (response.ok && data.status === 'success') {
          this.analysisStatus = 'Analysis completed successfully 🎉'

          // ⭐ 关键：iframe URL
          this.browserUrl = (data.ucsc_url || '').replace('localhost', '127.0.0.1')

          this.fetchResults()

          this.$nextTick(() => {
            this.$refs.browserSection?.scrollIntoView({ behavior: 'smooth' })
          })
        } else {
          this.analysisStatus = 'Analysis failed'
          this.errorMessage = data.error
        }

      } catch (error) {
        this.analysisStatus = 'Request failed'
        this.errorMessage = error.message
      } finally {
        this.running = false
      }
    },

    async fetchResults() {
      try {
        const response = await fetch(`${this.backendBase}/api/results`)
        const data = await response.json()

        if (response.ok && data.status === 'success') {
          this.results = data.files || []
        } else {
          this.results = []
        }
      } catch {
        this.results = []
      }
    }
  }
}
</script>

<style scoped>
.sqanti-page {
  margin: 0 auto;
  padding: 20px 40px;
  background: #ffffff;
  min-height: 100vh;
  box-sizing: border-box;
}

/* ===== Header ===== */
.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 8px;
}

.page-header p {
  color: #6b7280;
  font-size: 15px;
  line-height: 1.6;
}

/* ===== Card统一风格（参考你filter-container） ===== */
.card {
  background: #f6f6f6;
  border-radius: 12px;
  padding: 20px 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.card h2 {
  font-size: 20px;
  color: #2f3a4a;
  margin-bottom: 10px;
}

.desc {
  color: #6b7280;
  margin-bottom: 16px;
  font-size: 14px;
}

/* ===== Upload区域 ===== */
.upload-section {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}

/* ===== Button风格（完全对齐你另一个页面） ===== */
.primary-btn,
.secondary-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  border: none;
  cursor: pointer;
}

.primary-btn {
  background-color: #4e73df;
  color: white;
}

.primary-btn:hover {
  background-color: #3558c2;
}

.secondary-btn {
  background-color: #a0aec0;
  color: white;
}

.secondary-btn:hover {
  background-color: #7b8794;
}

.primary-btn:disabled,
.secondary-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

/* ===== 信息框 ===== */
.info-box,
.status-box,
.error-box,
.empty-box {
  margin-top: 14px;
  padding: 12px 14px;
  border-radius: 8px;
  font-size: 14px;
}

.info-box {
  background: #eef2ff;
  color: #3730a3;
}

.status-box {
  background: #f3f4f6;
  color: #374151;
}

.error-box {
  background: #fef2f2;
  color: #b91c1c;
}

.empty-box {
  background: #f8fafc;
  color: #64748b;
}

/* ===== Result列表 ===== */
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-list {
  list-style: none;
  padding: 0;
  margin-top: 14px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 12px 14px;
  border-radius: 8px;
  margin-bottom: 10px;
  border: 1px solid #e5e7eb;
}

.download-link {
  color: #4e73df;
  font-weight: 500;
  text-decoration: none;
}

.download-link:hover {
  text-decoration: underline;
}

/* ===== iframe 区域 ===== */
iframe {
  margin-top: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: inset 0 0 0 1px #e5e7eb;
}

.empty-visual-box {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder {
  text-align: center;
  color: #9ca3af;
}

.placeholder .icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.placeholder p {
  font-size: 16px;
  margin: 0;
}

.placeholder span {
  font-size: 13px;
  color: #c0c4cc;
}
</style>
