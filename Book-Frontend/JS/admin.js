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


const items = [];
fetch("http://localhost:5000/books/list")
  .then((res) => res.json())
  .then((data) => {
    data.data.forEach((d) => {
      console.log(d)
      const { name, isbn, price } = d;

      items.push({ isbn, name, price });
    });
    loadTable();
  });

const loadTable = () => {
  const row = document.createElement("tr");
  let cell = document.createElement("td");
  let cellText = document.createTextNode("Isbn");
  cell.appendChild(cellText);
  row.appendChild(cell);
  tableBody.appendChild(row);
  cell = document.createElement("td");
  cellText = document.createTextNode("Name");
  cell.appendChild(cellText);
  row.appendChild(cell);
  tableBody.appendChild(row);
  cell = document.createElement("td");
  cellText = document.createTextNode("Price");
  cell.appendChild(cellText);
  row.appendChild(cell);
  tableBody.appendChild(row);

  items.forEach((item) => {
    const row = document.createElement("tr");
    for (let key in item) {
      const cell = document.createElement("td");

      if (key != "isbn") {
        const input = document.createElement("input");
        input.type = "text";
        input.value = item[key];
        cell.appendChild(input);
        row.appendChild(cell);

        input.addEventListener("blur", async () => {
          console.log("hey")
          item[key] = input.value; // Update the item's value with the new input value

          const url = 'http://localhost:5000/books/update-book';

          const bookData = {};
          bookData[key] = item[key]

          if (key != "isbn")
            bookData["isbn"] = item["isbn"]

          const bearerToken = localStorage.getItem("access_token")
          const headers = new Headers();
          headers.append('Authorization', `Bearer ${bearerToken}`);
          headers.append('Content-Type', 'application/json');

          try {
            const response = await fetch(url, {
              method: 'POST',
              headers: headers,
              body: JSON.stringify(bookData),
            });

            const data = await response.json();

            if (data.success) {

            }
          } catch (error) {
            // Handle any errors that occurred during the fetch process
            console.error('Fetch error:', error);
          }

        });
      } else {
        const text = document.createElement("div");
        text.innerText = item[key];
        cell.appendChild(text);
        row.appendChild(cell);
      }



    }

    const deleteCol = document.createElement("td");
    const deleteText = document.createTextNode("Delete");
    deleteCol.appendChild(deleteText);
   
    deleteCol.style.color = "red";
    deleteCol.style.cursor = "pointer";

    const editCol = document.createElement("td");
    const editText = document.createTextNode("Edit");
    editCol.appendChild(editText);
    editCol.style.color = "red";
    editCol.style.cursor = "pointer";

    

    // set id as book_{isBn}
    deleteCol.addEventListener("click", function () {
      deleteColn(item?.isbn);
    });
    editCol.addEventListener("click", function(){
      window.location.href = "http://127.0.0.1:5500/Book-Frontend/edit.html?isbn=" + item?.isbn;
    });
    row.appendChild(editCol);
    
    row.appendChild(deleteCol);
    
    tableBody.appendChild(row);
  });
};

// delete post
const deleteColn = async (isbn) => {
  const confirmation = window.confirm("Are you sure you want to delete this cart?");

  if (confirmation) {
    const url = "http://localhost:5000/books/delete";
    const queryParams = new URLSearchParams({ isbn: isbn });
    const urlWithParams = `${url}?${queryParams}`;

    const bearerToken = localStorage.getItem("access_token")
    const headers = new Headers();
    headers.append('Authorization', `Bearer ${bearerToken}`);
    headers.append('Content-Type', 'application/json');

    try {
      const response = await fetch(urlWithParams, {
        method: 'GET',
        headers: headers,
      });

      const data = await response.json();

      if (data.success) {
        alert("Item deleted successfully");
        window.location.reload();
      }
    } catch (error) {
      console.error('Fetch error:', error);
    }
  }
};

// add new post
const handleAddPost = async (event) => {
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


  const url = 'http://localhost:5000/books/add-book';

  const bearerToken = localStorage.getItem("access_token")
  const headers = new Headers();
  headers.append('Authorization', `Bearer ${bearerToken}`);
  headers.append('Content-Type', 'application/json');

  // Perform the POST request using fetch
  async function bookAdd() {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(bookData),
      });

      const data = await response.json();

      if (data.success) {
        window.location.reload();
      }
    } catch (error) {
      // Handle any errors that occurred during the fetch process
      console.error('Fetch error:', error);
    }
  }

  bookAdd()
};

form.addEventListener('submit', handleAddPost);
