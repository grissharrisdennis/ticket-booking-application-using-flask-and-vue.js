<template>
  <header>
     <ul class="nav_links" >
      <li><span><h2>Show : {{ show.name }}</h2></span></li>
      <li><a><router-link   :to="{ name: 'UserDashboard', params: { id: this.$route.params.user_id}}">UserDashboard</router-link></a></li>
  </ul>
  </header>
<br>
<br>
 <div class="show" v-if="show">
      <div class="venue" v-for="venue in show.venues" :key="venue.id">
         <h3 > Available seats : {{ venue.capacity }}</h3>
        </div>
  </div>
   <br>
   <h4>Time :{{ show.show_time }}</h4>
   <br>
<form>
    <br>
    <div class="form-group">
    <label for="seats">No of Seats</label>
    <input type="number" id="seats" v-model="seats" name="seats" v-on:keyup="mult" >
  </div>
  

  <div class="form-group">
    <label for="price">Price</label>
    <input type="number" id="price" name="price"  :value="show.price"  readonly v-on:keyup="mult">
  </div>


   <div class="form-group">
    <label for="total">Total</label>
    <input type="text" id="total" name="total" :value="total"  readonly>
  </div>

<br>
<div class="form-group"></div>
  <input type="submit" @click="book_show">
</form>
<br>
</template>

<script>
export default {
    name:'BookingPage',
    data() {
    return {
      user_id: null,
      show:[],
      seats:null,
    };
  },
  mounted(){
    this.fetchShow();
  },
  methods:{
  fetchShow(){
      fetch(`http://127.0.0.1:5000/api/${this.$route.params.show_id}/get/show`, {
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
          if (result && Array.isArray(result) && result.length > 0) {
            this.show = result[0];
          }
          console.log(this.show)
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
 },
 mult(){
        var one = document.getElementById('seats').value;
        var two = document.getElementById('price').value;
        var result = parseFloat(one)* parseFloat(two);
        document.getElementById('total').value = result;
  },
 book_show() {
      const data = {
        seats:this.seats,
      };
      // const id =this.$route.params.user_id;
      const venue_id=this.$route.params.venue_id
      const show_id=this.$route.params.show_id
      if (this.show.venues && this.show.venues.length > 0) {
        const matchingVenue = this.show.venues.find(venue => venue.id === Number(venue_id));
        console.log('Matching Venue:', matchingVenue);
        if (!matchingVenue) {
          alert("Invalid Venue ID.");
          return; 
        }

        const venueCapacity = matchingVenue.capacity;
        if (parseInt(this.seats) > venueCapacity) {
          alert(`Number of seats exceeds available capacity. Maximum available seats: ${venueCapacity}`);
          return; 
      }
      fetch(` http://127.0.0.1:5000/api/post/book/${this.$route.params.user_id}/${venue_id}/${show_id}`, {
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
          this.$router.push({ name: 'UserDashboard', params: { id: this.$route.params.user_id } });
        })
        .catch(error => {
          console.error(error);
        });
    }
},
}
}
</script>

<style>
 span{
  margin-right: 800px;
 }
 h3{
  color:black;
 }
</style>