<template>
    <header>

<ul class="navi_links">
      <h1>Update Venue</h1>
      <li><a><router-link  :to="{ name: 'AdminDashboard', params: { id: $route.params.admin_id }}">DashBoard</router-link></a></li>
      <li><a @click="logout()">Logout</a></li>   
</ul>
</header>
<br>
<br>


<form >
    
    <br>
    <br>
  <div class="form-group">
    <label for="venue-name">Venue Name:</label>
    <input type="text" id="venue-name" v-model="name" name="venue-name">
  </div>

  <div class="form-group">
    <label for="venue-place">Place:</label>
    <input type="text" id="venue-place" v-model="place" name="venue-place">
  </div>

   <div class="form-group">
    <label for="venue-location">Location:</label>
    <input type="text" id="venue-location" v-model="location" name="venue-location">
  </div>

  <div class="form-group">
    <label for="venue-capacity">Capacity:</label>
    <input type="number" id="venue-capacity" v-model="capacity" name="venue-capacity">
  </div>

  <button type="submit"  @click="updateVenue">Save</button>
</form>
</template>

<script>
export default {
  name:"UpdateVenue",
  data() {
      return {
      name:'',
      place:'',
      location:'',
      capacity:''
    };
  },
methods:{
  updateVenue(){
    const venue_id=this.$route.params.venue_id;
    const data={
      name:this.name,
      place:this.place,
      location:this.location,
      capacity:this.capacity
    }
      fetch(`http://127.0.0.1:5000/api/${venue_id}/put/venue`, {
        method: 'PUT',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token'),
        },
        body: JSON.stringify(data),
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
          console.log(result.message); 
          this.$router.push(`/${this.$route.params.admin_id}/admin/dashboard`);
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
    },
  }
}
</script>

<style>
form {
  width: 400px;
  margin: auto;
}

/* Apply styles to each form group */
.form-group {
  margin-bottom: 15px;
}

/* Apply styles to labels */
label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

/* Apply styles to input fields */
input {
  width: 100%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

/* Apply styles to the submit button */
button[type="submit"] {
  background-color: #333;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>