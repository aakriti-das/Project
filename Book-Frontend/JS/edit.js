const tableBody = document.getElementById("table_body");
const form = document.getElementById("form");
const access_token = localStorage.getItem("access_token");

if (!access_token) {
  window.location.replace("admin-login.html");
}

const url = 'http://localhost:5000/get-profile';

const bearerToken = localStorage.getItem("access_token")
const headers = new Headers();
headers.append('Authorization', `Bearer ${bearerToken}`);
headers.append('Content-Type', 'application/json');

// Perform the POST request using fetch
async function getProfile() {
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: headers,

    });

    const data = await response.json();

    if (data.success) {
      if (data.data.type != "admin") {
        window.location.replace("admin-login.html");
      }
    }

  } catch (error) {
    console.error('Fetch error:', error);
  }
}

getProfile()


var item = null;
const urlParams = new URLSearchParams(window.location.search);
const currentIsbn = urlParams.get('isbn');
fetch("http://localhost:5000/books/get-book?isbn="+currentIsbn)
  .then((res) => res.json())
  .then((data) => {
    console.log(data.data);
    item = data.data;
    prefill();
  });

  function prefill(){
    document.getElementById("isbn").value = item.isbn;
    document.getElementById("book_name").value = item.name;
    document.getElementById("author_name").value = item.author_name;
    document.getElementById("category").value = item.category;
    document.getElementById("description").value = item.description;
    document.getElementById("image-url").value = item.image_url;
    document.getElementById("price").value = item.price;
    document.getElementById("published_date").value = item.published_date;
  }

  const handleUpdatePost  = async (event) => {
    event.preventDefault()
  
    const isbn = document.getElementById("isbn").value;
    const name = document.getElementById("book_name").value;
    const author_name = document.getElementById("author_name").value;
    const category = document.getElementById("category").value;
    const description = document.getElementById("description").value;
    const image_url = document.getElementById("image-url").value;
    const price = document.getElementById("price").value;
    const published_date = document.getElementById("published_date").value;
  
    const bookData = {
      isbn,
      name,
      author_name,
      category,
      description,
      image_url,
      price,
      published_date,
    };  
  
    const url = 'http://localhost:5000/books/update-book';
  
    const bearerToken = localStorage.getItem("access_token")
    const headers = new Headers();
    headers.append('Authorization', `Bearer ${bearerToken}`);
    headers.append('Content-Type', 'application/json');
  
    // Perform the POST request using fetch
    async function bookUpdate() {
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: headers,
          body: JSON.stringify(bookData),
        });
  
        const data = await response.json();

        console.log(data);
  
        if (data.success) {
            window.location.href = "http://127.0.0.1:5500/Book-Frontend/admin.html";
        }
      } catch (error) {
        // Handle any errors that occurred during the fetch process
        console.error('Fetch error:', error);
      }
    }
    // sth
    bookUpdate();
    };


  form.addEventListener('submit', handleUpdatePost);
