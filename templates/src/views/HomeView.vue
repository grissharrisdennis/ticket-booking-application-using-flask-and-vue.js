<template>
  <NavBar></NavBar> 
  <div class="home">
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
export default {
  name: 'HomeView',
  components: {
    NavBar,
  },
}
</script>
<style>
.home{
  height:800px;
  background: url('../assets/terminator.jpg'),url('../assets/jones.jpg'),url('../assets/lagaan.jpg');
  background-repeat: no-repeat,no-repeat;
  padding: 15px;
  background-position: left,center,right;
  background-size: contain;
}
</style>