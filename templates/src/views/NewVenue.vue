<template>
 <header>

<ul class="navi_links">
      <h1>Create Venue</h1>
      <li><a><router-link  :to="{ name: 'AdminDashboard', params: { id: $route.params.id }}">DashBoard</router-link></a></li>
      <li><a @click="logout()">Logout</a></li>   
</ul>
</header>
<br><!-- {% for venue_key, venue_value in data.venues.items() %} -->
<div class="venue">
<form >
    <h1>Create Venue</h1>
    <br>
  <div class="form-group">
    <label for="venue-name">Venue Name:</label>
    <input type="text" id="venue_name" v-model="venue_name" name="venue_name">
  </div>

  <div class="form-group">
    <label for="venue-place">Place:</label>
    <input type="text" id="venue_place" v-model="venue_place" name="venue_place">
  </div>

  <div class="form-group">
    <label for="venue-location">Location:</label>
    <input type="text" id="venue_location" v-model="venue_location"  name="venue_location">
  </div>

  <div class="form-group">
    <label for="venue-capacity">Capacity:</label>
    <input type="number" id="venue_capacity" v-model="venue_capacity" name="venue_capacity">
  </div>
<br>
  <input type="submit" @click="create_venue">
</form>
</div>
</template>

<script>
export default {
    name:"NewVenue",
  data() {
    return {
      venue_name: '',
      venue_place: '',
      venue_location:'',
      venue_capacity:'',
    };
  },
  methods: {
    create_venue() {
      const data = {
        venue_name: this.venue_name,
        venue_place: this.venue_place,
        venue_location:this.venue_location,
        venue_capacity: this.venue_capacity
      };

      
      fetch(` http://127.0.0.1:5000/api/post/venue`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('token')
        },
        body: JSON.stringify(data),
      })
        .then(response => response.json())
        .then(result => {
          console.log(result.message);
          this.$router.push(`/${this.$route.params.id}/admin/dashboard`)
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
}

</script>

<style>
		/* Apply general styles to the form */
form {
   width: 400px;
   margin: 50px auto;
   align-items: center;
   padding: 20px;
   border: 2px solid #333;
   border-radius: 10px;
	box-shadow: 0 0 10px #333;

}

/* Apply styles to each form group */
.form-group {
  align-items:center;
  margin-bottom: 15px;
}
h1{
text-align:center;
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
input[type="submit"] {
			background-color: #333;
			color: #fff;
			padding: 10px 20px;
			border: none;
			border-radius: 4px;
			font-size: 16px;
			cursor: pointer;
			transition: all 0.3s ease;
		}

		input[type="submit"]:hover {
			background-color: #fff;
			color: #333;
		}


</style>