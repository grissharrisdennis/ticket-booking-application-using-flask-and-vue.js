<template>
  <NavBar></NavBar>
  <div class="login-dark">
    
  <form @submit.prevent="login">
    <br>
      <h5>Login</h5>
    <br>
    <br>
    <div class="input-group">
      <label for="username">Username</label>
      <input type="username" id="username" v-model="username" placeholder="Enter your username">
    </div>
      <br>
      <br>
    <div class="input-group">
      <label for="password">Password</label>
      <input type="password" id="password" v-model="password" placeholder="Enter your password">
    </div>
      <br>
      <br>
      <br>
      <button type="log-in-button" >Log In</button>
      <br>
      <br>
      <h4>Not Registered</h4>
      <a><router-link to="/register">Sign Up</router-link></a> 
    </form>
  </div>
  
</template>

<script>
import NavBar from '@/components/NavBar.vue';
export default {
  components: {
    NavBar,
  },
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    login() {
      const data = {
        username: this.username,
        password: this.password,
      };

      fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then(response => {
          console.log(response); // Log the response to inspect it
          return response.json();
        })
        .then(result => {
          // Handle the login response
          console.log(result.token);

          if (result.message === 'User Successfully Logged In') {
            localStorage.setItem('token', result.token);
            this.$router.push(`/${result.id}/user/dashboard`);
          } else if (result.message === 'Admin Successfully Logged In') {
            localStorage.setItem('token', result.token);
            this.$router.push(`/${result.id}/admin/dashboard`);
          }
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};

</script>

<style>
 .login-dark {
  height:800px;
  background: url('../assets/terminator.jpg'),url('../assets/jones.jpg'),url('../assets/lagaan.jpg');
  background-repeat: no-repeat,no-repeat;
  padding: 15px;
  background-position: left,center,right;
  background-size: contain;
  
}
.login-dark form {
  width: 500px;
  height:600px;
  padding: 20px;
  position: static;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin: 0 auto;
  background: #283c86;
  position: relative;
  top: 140px;
}
.login-dark h5{
  color:#fff;
  font-size:40px;
}
.h2{
  position:relative
}
.input-group {
    margin-bottom: 15px;
  }
  
  .input-group label {
    display: block;
    color:#fff;
    margin-bottom: 5px;
  }
  
  .input-group input {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }

  button[type="log-in-button"] {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    border: none;
    background-color: #4caf50;
    color: white;
    cursor: pointer;
  }

  button[type="log-in-button"]:hover{
    background-color:#000;
  }
</style>

