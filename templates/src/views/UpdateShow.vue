<template>
   <header>

<ul class="navi_links">
      <h1>Update Show</h1>
      <li><a><router-link  :to="{ name: 'AdminDashboard', params: { id: $route.params.admin_id }}">DashBoard</router-link></a></li>
      <li><a @click="logout()">Logout</a></li>   
</ul>
</header>
<br>
<br>

<form enctype="multipart/form-data">
    <br>
	<label for="name">Show Name:</label>
	<input type="text" id="name" name="name" v-model="name" required>

	<label for="rating">Rating:</label>
	<input type="number" id="rating" name="rating" v-model="rating" min="0" max="10" step="0.1" required>

	<label for="tags">Tags:</label>
	<input type="text" id="tags" name="tags" v-model="tags" required>

	<label for="show_time">Show Time:</label>
    <input type="datetime-local" id="show_time" v-model="show_time" name="show_time" required>

	<label for="ticketprice">Ticket Price:</label>
	<input type="number" id="ticketprice" name="ticketprice" v-model="ticketprice" min="0" required>

	<div class="form-group">
		<label for="image_file">Image File</label>
		<input type="file" class="form-control-file"  @change="select_image($event)" id="image_file" name="image_file">
	</div>

	<input type="submit" @click="update_show">
	</form>

</template>

<script>
export default {
	name:"UpdateShow",
methods:{
	select_image(event){
		const file = event.target.files[0];
		this.image_file=file
		console.log("image",this.image_file)
	},
	async update_show() {
      const formData = new FormData();
      formData.append("name", this.name);
      formData.append("rating", this.rating);
      formData.append("tags", this.tags);
      formData.append("show_time", this.show_time);
      formData.append("ticketprice", this.ticketprice);
      formData.append("image_file", this.image_file);
	const show_id=this.$route.params.show_id;
      const venue_id = this.$route.params.venue_id;
                       
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/${venue_id}/${show_id}/put/show`, {
          method: "PUT",
          headers: {
            Accept: "application/json",
            "Authentication-Token": localStorage.getItem("token"),
          },
          body: formData,
        });
        if (!response.ok) {
          const errorMessage = await response.text();
          console.error("Error from backend:", errorMessage);
          return;
        }
        const data = await response.json();
        console.log(data.message);
        this.$router.push(`/${this.$route.params.admin_id}/admin/dashboard`);
      } catch (error) {
        console.error("Error while sending the request:", error);
        // Handle error cases
      }
    },
  },
}
</script>

<style>
form {
			display: flex;
			flex-direction: column;
			align-items: center;
			padding: 20px;
			border: 2px solid #333;
			border-radius: 10px;
			box-shadow: 0 0 10px #333;
			width: 400px;
			margin: 50px auto;
		}

		input[type="text"], input[type="number"] {
			padding: 10px;
			margin: 10px 0;
			border: none;
			border-bottom: 2px solid #333;
			width: 100%;
			font-size: 16px;
		}

		input[type="submit"] {
			background-color: #333;
			color: #fff;
			padding: 10px 20px;
			border: none;
			border-radius: 5px;
			font-size: 16px;
			cursor: pointer;
			transition: all 0.3s ease;
		}

		input[type="submit"]:hover {
			background-color: #fff;
			color: #333;
		}
</style>