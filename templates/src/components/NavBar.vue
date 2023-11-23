<template>
    <nav >
      <router-link to="/">Home</router-link> 
      <router-link to="/login">Login</router-link> 
      <router-link to="/register">Sign Up</router-link> 
    </nav>
    <router-view/>
</template>

<script>
export default {
  name:"NavBar"
}
</script>

<style>
nav {
  background: #2c3e50;
  height:50px;
  padding-top: 10px;
  padding-bottom:20px;
}
nav a {
  font-weight: bold;
  text-decoration: none;
  color:#999;
  font-size: 30px;
  padding:70px;
}

nav a.router-link-exact-active {
  color: #42b983;
} 

</style>
<!-- 
 -->
