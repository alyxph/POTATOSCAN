<template>
  <div id="app">
    <navbar />
    <scan />
    <featurecard />
  </div>
</template>

<script>
import navbar from './component/navbar.vue';
import scan from './component/scan.vue';
import featurecard from './component/featurecard.vue';

export default {
  components: {
    navbar,
    scan,
    featurecard
  }
}
</script>

<style>
</style>

