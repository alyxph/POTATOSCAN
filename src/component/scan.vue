<template>
<div class="bg-gray-100 p-8">
  <div class="max-w-xl p-6 bg-white shadow-md mx-auto relative rounded-xl">
    <p class="text-lg bold mb-4 text-center">Upload Your Potato Photo</p>
    <div class="">
      <div class="flex items-center justify-center w-full">
        <label @drop.prevent="handleFileDropped" @dragenter="startDrag" @dragover.prevent="() => {}" @dragleave="leaveDrag" for="dropzone-file" :class="['flex flex-col items-center justify-center w-full h-64 border-gray-900 border-2 border-dashed rounded-lg cursor-pointer', {'bg-blue-50 hover:bg-blue-50 border-blue-600': activeDrag}, {'bg-zinc-50 hover:bg-zinc-100 border-gray-300': !activeDrag}]">
          <div class="flex flex-col items-center justify-center pt-5 pb-6 pointer-events-none">
              <svg :class="['w-8 h-8 mb-4 text-gray-900 dark:text-gray-900', {'text-blue-600': activeDrag}]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
              </svg>
              <p :class="['pointer-events-none mb-2 text-sm text-gray-900 dark:text-gray-900', {'text-blue-600': activeDrag}]"><span class="font-semibold">Click to upload</span> or drag and drop</p>
          </div>
          <input id="dropzone-file" type="file" class="hidden" accept=".pdf,.jpg,.jpeg,.png"/>
        </label>
      </div> 
      <div class="flex justify-between mt-2">
        <p class="text-xs text-gray-900">Supported Formats: JPG, JPEG, PNG</p>
        <p class="text-xs text-gray-900">Max size: 25MB</p>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      documents: ["", "", ""],
      activeDrag: false,
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
      const file = JSON.stringify(event.dataTransfer);
      console.log(event);
      console.log(file);
    }
  }
};
</script>

<style>

</style>