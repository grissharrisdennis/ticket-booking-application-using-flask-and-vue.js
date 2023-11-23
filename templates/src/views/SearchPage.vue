<template>
  <div class="search">
  <header>
    <ul class="nav_links">
      <li><h2>Search Results</h2></li>
      <li><a ><router-link  :to="{ name: 'UserDashboard', params: { id: this.$route.query.user_id}}">UserDashboard</router-link></a></li>
      <li><a @click="logout()">Logout</a></li>
    </ul>
</header>
    <div class="boxes" v-for="venues in venue"   :key="venues.id">
      <div class="ven" v-if="this.$route.params.id==venues.id">
        <h1 class="name">{{ venues.name }}</h1>
        <br>
        <div class="carde" v-for="shows in venues.shows" :key="shows.show_id">
        <img v-bind:src="getImageUrl(shows.image_file)">
        <router-link   :to="{ name: 'BookingPage', params: { venue_id:this.$route.params.id,show_id: shows.id, user_id:this.$route.query.user_id }}">
          <button class="cards-btn" v-bind:disabled="houseful(venues.capacity) === true">
            {{ venues.capacity < 1 ? 'Houseful' : 'Book' }}
          </button>
        </router-link>
        <h2>{{ shows.name }}</h2>
        </div>
        <br>
      </div>
    </div>
    <div class="boxes" v-if="show" >
      <div class="carde" v-for="shows in show" :key="shows.id">
          <img v-bind:src="getImageUrl(shows.image_file)"  alt="Description of the image"> 
          <div class="texts">
            <h2>{{ shows.name }}</h2>
            <div class="showven" v-for="venuess in shows.venues" :key="venuess.id">
              <router-link  :to="{ name: 'BookingPage', params: { venue_id:venuess.id,show_id: shows.id, user_id:this.$route.query.user_id }}"><button class="cards-btn">Book</button></router-link>
            </div>
          </div>
      </div>
    </div>
    <!-- <div class="boxes" v-if="show" >
      {{ show.name }}
      <div class="carde" >
      <img v-bind:src="getImageUrl(show.image_file)"  alt="Description of the image"> 
        <div class="text">
          <h2>{{ show.name }}</h2>
          <div class="showven" v-for="venuess in show.venues" :key="venuess.id">
          <router-link  :to="{ name: 'BookingPage', params: { venue_id:venuess.id,show_id: this.$route.params.id, user_id:this.$route.query.user.id }}"><button class="btn">Book</button></router-link>
        </div>
      </div>
        <br>
      </div>
    </div> -->
  </div>
</template>

<script>
export default {
    name:'SearchPage',
    data(){
      return {
      user: null,
      venue:null,
      show:null,
    };
    },
  mounted() {
    this.fetchVenue();
    this.fetchShow();
  },
  methods:{
    houseful(capacity){
      console.log(capacity)
      if (capacity <= 0 || !Number.isInteger(capacity)) {
        return true;
      } else {
        return false;
      }
    },
    getImageUrl(imageFile) {
      console.log(imageFile)
      return require(`../assets/images/${imageFile}`)
    },
    fetchVenue(){
      fetch(`http://127.0.0.1:5000/api/get/venue`, {
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
            this.venue = result;
          }
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
    },
    fetchShow(){
      fetch(`http://127.0.0.1:5000/api/${this.$route.params.id}/get/show`, {
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
            this.show = result;
            console.log(this.show)
            const show = this.show;
            console.log(show)
          }
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
    },
    logout() {
      // Send the logout request to the server
      fetch(' http://127.0.0.1:5000/api/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('token'),
        },
      })
        .then(response => response.json())
        .then(result => {
          console.log(result);
          if (result.message === 'Logged out') {
            console.log("Logout successful");
            localStorage.setItem('token', "null");
            this.$router.push(`/login`);
          } else {
            console.log("Logout failed");
          }
        })
        .catch(error => {
          console.error(error);
          
        });
    }
  }
}
</script>

<style>
.boxes{
  width:100%;
  margin:50px auto;
  border-radius:20px;
  background: #232526;  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #414345, #232526);  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #414345, #232526); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
.boxes h1{
  font-size:40px;
  color:white;
  font-weight: 200px;
}
.carde{
  width:300px;
  align-items: center;
  text-align: center;
  margin-left: 30px;
  margin-bottom: 40px;
  border:1px solid grey;
  background: black;
}
.carde img{
  width:100%;
}
.carde .btn {
  position: absolute;
  top: 70%;
  left: 13%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  background-color: #f1f1f1;
  color: black;
  font-size: 16px;
  padding: 16px 30px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  text-align: center;
}
.carde .btn:hover {
  background-color: black;
  color: white;
}
.text{
  padding:5px;
  background-color:#fff;
}
.texts{
  padding:5px;
  background-color:#000;
}
.carde h2{
  color:white;
}
ul li h2{
  margin-right: 500px;
  font-size:40px;
}
ul li a{
  font-size:20px;
}
</style>