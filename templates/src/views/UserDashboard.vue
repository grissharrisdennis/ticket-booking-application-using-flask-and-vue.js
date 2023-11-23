<template>
<div class="user" v-if="user">
  <header>

<ul class="nav_links">
      <h1>Welcome {{ user.username }} <p>Email:{{ user.email }}</p> </h1>
      <li><a ><router-link   :to="{ name: 'UserBookings', params: { id: user.id }}">UserBookings</router-link></a></li>
      <li><a @click="logout()">Logout</a></li>
      <li>
        <a>
          <div class="searchbox">
              <input type="search" name="search_query" v-model="query" id="search_query" >
              <button type="submit" @click="search" class="fa fa-search">Search</button>
          </div>
        </a>
      </li>

</ul>
</header>



  <div class="trick">
      <br>
      <br>
    <div class="navigator">
    <div class="sections" v-for="venues in venue"   :key="venues.id">
      <br> 
          <h3>{{ venues.name }}</h3>
          <div class="cards" v-for="shows in venues.shows" :key="shows.show_id">
            <img class="cards-img" v-bind:src="getImageUrl(shows.image_file)">
            <div class="cards-body">
              <h1 class="cards-title">{{ shows.name }}</h1>
              <h4 class="cards-sub-title">Time: {{ shows.show_time }}</h4>
              <p class="cards-info">Genre: {{ shows.tags }}</p>

            
                    <router-link :to="{ name: 'BookingPage', params: { user_id: user.id, venue_id: venues.id, show_id: shows.id }}">
                      <button class="cards-btn" :disabled="houseful(venues.capacity)">
                        {{ venues.capacity < 1 ? 'Housefull' : 'Book' }}
                      </button>
                    </router-link>
                  
            </div>
          </div>     
        <br>
    </div>
    <br>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'UserDashboard',
  data() {
    return {
      user: null,
      venue:null,
      error: null,
      query:null,
      message:'',
      capacity:0,
    };
  },
  mounted() {
    this.fetchUser();
    this.fetchVenue();
    this.houseful();
  },
  methods: {
    houseful(capacity){
      console.log(capacity)
      if (capacity <= 0) {
        return true;
      } else {
        return false;
      }
    },
    getImageUrl(imageFile) {
      return require(`../assets/images/${imageFile}`)
    },
    fetchUser() {
      const id = this.$route.params.id;
      fetch(`http://127.0.0.1:5000/api/${id}/user`, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token'),
        }
      })
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Network response was not OK');
          }
        })
        .then(result => {
          console.log(result); // Log the entire result object
          if (result && result.email && result.id && result.username) {
            this.user = result;
          }
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
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
          console.log(result); // Log the entire result object
          if (result) {
            this.venue = result;
          }
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
    },
    search(){
      const data = {
        query: this.query,
      };

      fetch(`http://127.0.0.1:5000/api/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('token'),
        },
        body: JSON.stringify(data),
      })
        .then(response => {
          if (response.ok) {
            console.log(response);
            return response.json();
          } else {
            throw new Error('Network response was not OK');
          }
        })
        .then(result => {
          console.log(result);
          if (result.message === 'search is successful') {
            console.log("search successful");
            // Redirect to the search page with the search query as a query parameter
            this.$router.push({ name: 'SearchPage',params:{ user_id: this.$route.params.id, id: result.id }, query: { user_id: this.$route.params.id, id: result.id } });
          } else {
            console.log("Search failed");
          }
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
    },
    logout() {
      // Send the login request to the server
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
  },
};
</script>
<style>
.user{
 margin:0;
 padding:0;
 box-sizing:border-box;
 background:#eee;
 font-family:Arial;
 }
 .navigator{
 margin:0;
 padding:0;
 box-sizing:border-box;
 }
 .sections{
 width:100%;
 height:100%;
 justify-content:space-around;
 align-items:center;
 display: flex;
  flex-wrap: wrap;
  margin-left:30px;
  padding-top: 60px;
  max-width: 400px;
  padding-left:30px;
  padding-right:30px;
  padding-bottom:30px;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-shadow: 0 5px 10px rgba(0,0,0,0.1);
  background:url('../assets/o.jpeg');
 }
 .sections h3{
 text-align:center;
 padding-bottom:30px;
 font-size:40px;
 color: #ccc;


 }
 .cards{
  width:320px;
  height:500px;
  overflow:hidden;
  border-radius:8px solid #fff ;
  position: relative;
 }
 .cards-img{
  width: 100%;
  height: 100%;
  object-fit: cover;
 }
 .cards-body{
  width: 100%;
  height: 100%;
  top:0;
  right:-100%;
  position:absolute;
  background: #00000013;
  backdrop-filter: blur(5px);
  border-radius:15px;
  color:#fff;
  padding:30px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition:2s;
 }
 .cards:hover .cards-body{
  right:0;

 }
 .cards-title{
  text-transform:uppercase;
  font-size:50px;
  font-weight:500;
 }
 .cards-sub-title{
  text-transform:uppercase;
  font-size:20px;
  font-weight:300;
 }
 .cards-info{
  font-size:16px;
  line-height:25px;
  font-weight:400;
  margin:40px 0;
 }
 .cards-btn{
  color:#1f3d47;
  background:#8fabba ;
  text-decoration: none;
  padding:10px;
  text-transform: capitalize;
  font-weight:500px;
  border:none;
  outline:none;
  cursor:pointer;
  width:120px;
  color:#fff;
 }

.searchbox {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

input[type=search] {
  padding: 10px;
  font-size: 17px;
  border: 2px solid #ccc;
  border-radius: 4px;
  transition: width 0.4s ease-in-out;
  width: 60px;
}

input[type=search]:focus {
  width: 200px;
}

button[type=submit] {
  border: none;
  background: #101010;
  cursor: pointer;
}

.fa-search {
  font-size: 20px;
  color: #ccc;
  transition: color 0.4s ease-in-out;
}

input[type=search]:focus + button .fa-search {
  color: #000;
}

header{
display:flex;
justify-content:flex-end;
align-items:center;
padding:10px 10%;
background-color:#000;
}
.logo {
cursor:pointer;
margin-right:auto;
}
.nav_links{
list-style:none;
}
.nav_links li{
display:inline-block;
padding:10px 10px;
}
.nav_links h1{
  font-size: 40px;
  float: left;
  margin-right: 500px;
  color:white
}
.nav_links h1 p{
  font-size: 15px;
}
.nav_links li a{
  text-decoration: none;

  color:#eee;
  transition:all 0.3s ease 0s;
}
.nav_links li a:hover{
  background-color:#eee;
  color:#000;
}
button{
padding:ppx 25px;
background-color:rgba(o,136,169,1);
border:none;
border-radius:50px;
cursor:pointer;
transition:all 0.3s ease 0s;
}
button:hover{
background-color:rgba(0,136,189,0.8);
}
.trick{
background-image:url('../assets/white.jpg');
background-size:cover;
}
</style>
