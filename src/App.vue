<template>
  <div id="app">
    <navbar />
    
    <!-- View Switcher -->
    <scan 
      v-if="currentView === 'home'" 
      @process-complete="handleProcessComplete" 
    />
    
    <process-result 
      v-if="currentView === 'result'" 
      :result="resultData" 
      @back="currentView = 'home'"
    />
    
    <featurecard v-if="currentView === 'home'" />
  </div>
</template>

<script>
import navbar from './component/navbar.vue';
import scan from './component/scan.vue';
import featurecard from './component/featurecard.vue';
import ProcessResult from './component/processResult.vue';

export default {
  components: {
    navbar,
    scan,
    featurecard,
    ProcessResult
  },
  data() {
    return {
      currentView: 'home', // 'home' or 'result'
      resultData: null
    }
  },
  methods: {
    handleProcessComplete(data) {
      this.resultData = data;
      this.currentView = 'result';
      // Scroll to top to make it feel like a new page load
      window.scrollTo(0, 0);
    }
  }
}
</script>

<style>
</style>
