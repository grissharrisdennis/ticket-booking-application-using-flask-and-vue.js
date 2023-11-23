<template>
<header>

<ul class="navi_links">
      <h1>Show Summary</h1>
      <li><a><router-link  :to="{ name: 'AdminDashboard', params: { id: $route.params.id }}">DashBoard</router-link></a></li>
      <li><a @click="logout()">Logout</a></li>   
</ul>
</header>
<br>
<br>
  <h3 class="plot">Shows vs No of seats</h3>
  <img :src="getImageSource(plot)" alt="Summary Image" class="center">
      
</template>

<script>
export default {
    name:'SummaryPage',
    data() {
    return {
      plot: '',
    };
  },
  mounted(){
      this.fetchplot();
  },
    methods:{
      fetchplot(){
      fetch(`http://127.0.0.1:5000/api/generate_summary`, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token'),
        }
      })
        .then(response => {
          if (response.ok) {
            console.log(response)
            return response.json();
          } else {
            throw new Error('Network response was not OK');
          }
        })
        .then(result => {
          console.log(result);
          if (result) {
            this.plot = result;
          }
          console.log(this.plot)
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
 },
 getImageSource() {
      // Construct the image source using the base64-encoded plot data
      if (this.plot) {
        return `data:image/png;base64, ${this.plot}`;
      } else {
        return '';
      }
    }
    }
}
</script>

<style>

 .plot{
  font-size:26px;
 }
 .center {
display: block;
margin-left: auto;
margin-right: auto;
width: 50%;
}
</style>