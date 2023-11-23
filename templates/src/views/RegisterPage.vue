<template>
  <NavBar></NavBar>
  <div class="register">
    
    <div class="register-box">
      <form class="mx-1 mx-md-4"> 
        <br>    
        <h5>Sign Up</h5>
    <br>
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
    <div class="input-group">
      <label for="email">Email</label>
      <input type="email" id="email" v-model="email" placeholder="Enter your email">
    </div>
    <br>
    <br>
    <div class="input-group">
      <label>Select The Format For Monthly Reports:</label>
      <br>
      <fieldset>
        <legend>
    <label for="pdf">PDF</label>
    <input
      type="radio"
      id="pdf"
      v-model="reportType"
      value="pdf"
      name="reportType"
    />
  </legend>
  <legend>
    <label for="html">HTML</label>
    <input
      type="radio"
      id="html"
      v-model="reportType"
      value="html"
      name="reportType"
    />
  </legend>
  </fieldset>
    </div>
    <button class="sign-up-button" @click="signup">Sign Up</button>
    <br>
     </form>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
export default {
    name:'RegisterPage',
    components: {
    NavBar,
  },
    data() {
    return {
      username: '',
      password: '',
      email:'',
      reportType:'',
    };
  },
  methods: {
    signup() {
      
      const data = {
        username: this.username,
        password: this.password,
        email:this.email,
        reportType:this.reportType,
      };

      
      fetch(' http://127.0.0.1:5000/api/user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then(response => response.json())
        .then(result => {
          
          console.log(result);
          this.$router.push('/login')
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
}
</script>

<style>
.register {
  height:900px;
  background: url('../assets/coco.jpg'),url('../assets/R.jpg'),url('../assets/venom.jpg');
  background-repeat: no-repeat,no-repeat;
  padding: 15px;
  background-position: right,center,left;
  background-size: contain;
  
}
.register-box form{
    width: 500px;
    height:700px;
    padding: 20px;
    position: static;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin: 0 auto;
    background: #283c86;
    position: relative;
    top: 140px;
  }
  
  .register-box h5 {
  color:#fff;
  font-size:40px;
   
  }
  .input-group-radio input {
    /* width: 100%;
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid #ccc; */
    margin: 0.4rem;
  }
  .input-group-radio label {
    font:
    1rem 'Fira Sans',
    sans-serif;
    /* display: inline-block; */
    color:#ccc;
}
.radio-container {
  display: inline-flex; /* Use inline-flex to display the radio inputs in the same line */
  align-items: center; /* To vertically center the radio inputs with the labels */
  gap: 10px; /* Adjust the gap between radio inputs and labels as needed */
}
  .input-group {
    margin-bottom: 15px;
  }
  .input-group label {
    display: block;
    color:#ccc;
    margin-bottom: 5px;
  }
  
  .input-group input {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  
  .sign-up-button {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    border: none;
    background-color: #4caf50;
    color: white;
    cursor: pointer;
  }
  .sign-up-button:hover{
    background-color:#000;
  }
   
</style>