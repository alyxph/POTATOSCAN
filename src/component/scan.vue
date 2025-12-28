<template>
<div class="bg-gray-100 p-8">
  <div class="max-w-xl p-6 bg-white shadow-md mx-auto relative rounded-xl">
    <p class="text-lg bold mb-4 text-center">Unggah Foto Kentang Anda</p>
    <div>
      <div class="flex items-center justify-center w-full">
        <label 
          @drop.prevent="handleFileDropped" 
          @dragenter="startDrag" 
          @dragover.prevent="() => {}" 
          @dragleave="leaveDrag" 
          for="dropzone-file" 
          :class="['flex flex-col items-center justify-center w-full h-64 border-gray-900 border-2 border-dashed rounded-lg cursor-pointer transition-colors', {'bg-blue-50 border-blue-600': activeDrag}, {'bg-zinc-50 hover:bg-zinc-100 border-gray-300': !activeDrag}]"
        >
          <div class="flex flex-col items-center justify-center pt-5 pb-6 pointer-events-none">
              <svg :class="['w-8 h-8 mb-4 text-gray-900', {'text-blue-600': activeDrag}]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
              </svg>
              <p :class="['pointer-events-none mb-2 text-sm text-gray-900', {'text-blue-600': activeDrag}]"><span class="font-semibold">Klik untuk mengunggah</span> atau seret dan lepas</p>
          </div>
          <input id="dropzone-file" type="file" class="hidden" accept=".jpg,.jpeg,.png" @change="handleFileSelected" />
        </label>
      </div> 
      <div class="flex justify-between mt-2 mb-4">
        <p class="text-xs text-gray-900">Format yang Didukung: JPG, JPEG, PNG</p>
        <p class="text-xs text-gray-900">Ukuran maks: 25MB</p>
      </div>

      <!-- Loading Step -->
      <div v-if="loading" class="text-center py-4">
        <p class="text-blue-600 font-semibold animate-pulse">Sedang Memproses...</p>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="text-center py-4 bg-red-50 rounded-lg mt-4 border border-red-200">
        <p class="text-red-600">{{ error }}</p>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      activeDrag: false,
      selectedFile: null,
      loading: false,
      error: null
    };
  },
  mounted() {
    window.addEventListener("drop", function(e) {
      e = e || event;
      e.preventDefault();
    }, false);
  },
  methods: {
    startDrag(event) {
      event.preventDefault();
      this.activeDrag = true;
    },
    leaveDrag(event) {
      event.preventDefault();
      this.activeDrag = false;
    },
    handleFileDropped(event) {
      event.preventDefault();
      this.activeDrag = false;
      if (event.dataTransfer.files && event.dataTransfer.files[0]) {
        this.selectedFile = event.dataTransfer.files[0];
        this.uploadFile();
      }
    },
    handleFileSelected(event) {
      if (event.target.files && event.target.files[0]) {
        this.selectedFile = event.target.files[0];
        this.uploadFile();
      }
    },
    async uploadFile() {
      if (!this.selectedFile) return;

      this.loading = true;
      this.error = null;

      const formData = new FormData();
      formData.append('image', this.selectedFile);

      try {
        const response = await fetch('http://localhost:5000/classify', {
          method: 'POST',
          body: formData
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || 'Terjadi kesalahan saat memproses gambar');
        }

        // Emit event to parent to handle "redirect"
        this.$emit('process-complete', data);
        
      } catch (err) {
        console.error("Upload error:", err);
        this.error = "Gagal memproses gambar. Pastikan backend server berjalan.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style>

</style>