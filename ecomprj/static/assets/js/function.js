console.log("working fine");
const monthname = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Auc",
  "Nov",
  "Dec",
];

// review

// Content for different navigation items

// Handle navigation click
document.querySelectorAll(".nav-link").forEach((navLink) => {
  navLink.addEventListener("click", (e) => {
    e.preventDefault();
    // Update active link
    document
      .querySelectorAll(".nav-link")
      .forEach((link) => link.classList.remove("active"));
    navLink.classList.add("active");

    // Update content area
    const contentKey = navLink.getAttribute("data-content");
    document.getElementById("content-area").innerHTML = contents[contentKey];
  });
});

$("#comment").submit(function (e) {
  e.preventDefault(); //prevent refresh

  let db = new Date();
  let time =
    db.getDate() + " " + monthname[db.getUTCMonth()] + " " + db.getFullYear();

  //Now to get data filled in form

  $.ajax({
    data: $(this).serialize(), //all the data from the form

    method: $(this).attr("method"), //methos from comment id div

    url: $(this).attr("action"),

    dataType: "json",

    success: function (res) {
      //resonse from the server
      console.log("Comment saved in db");

      let user = res.context.user; // Assuming user is "rohan"
      let formattedUser =
        user.charAt(0).toUpperCase() + user.slice(1).toLowerCase();

      if (res.bool == true) {
        //as it it always true when you get response
        $("#review_resp").html("Review Added Successfully");
        $(".hide_form").hide();
        $(".hide_review").hide();

        let _html = '<div class="media mb-4">';

        let classes = "img-fluid mr-3 mt-1";
        _html += `<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTr3jhpAFYpzxx39DRuXIYxNPXc0zI5F6IiMQ&s" alt="Image" class="${classes}" style="width: 45px;" />`;

        _html += '<div class="media-body">';
        _html +=
          "<h6 title='" +
          formattedUser +
          "'>" +
          formattedUser +
          "<small> - <i>" +
          time +
          "</i></small>" +
          "</h6>";
        _html += "</h6>";

        _html += '<div class="text-primary mb-2">';
        for (let i = 1; i <= res.context.rating; i++) {
          _html += '<i class="fas fa-star"></i>';
        }

        _html += "</div>";

        _html += "<p>" + res.context.review + "</p>";

        _html += "</div>";
        _html += "</div>";

        $(".review_col").prepend(_html);
      }
    },
  });
});

$(document).ready(function () {
  // Fetch the CSRF token from the meta tag
  const csrftoken = $("meta[name='csrf-token']").attr("content");

  $(".filter-checkbox, #price-range-btn").on("click", function () {
    console.log("checkbox have been clicked");
    console.log($(".filter-checkbox").length);

    let filter_object = {};

    let min_price = $("#max_price1").attr("min");
    let max_price = $("#max_price1").val(); // current price

    filter_object.min_price = min_price;
    filter_object.max_price = max_price;

    $(".filter-checkbox").each(function () {
      let filter_val = $(this).val();
      let filter_data = $(this).data("filter"); // data-filter / data-rohan ...   category vendor

      console.log("filter val", filter_val); //id             // getting all value id from tag
      console.log("filter data", filter_data); // getting data from tag data-filter

      filter_object[filter_data] = Array.from(
        document.querySelectorAll(
          "input[data-filter = " + filter_data + "]:checked" // filter out that query(filter we have choose - checked) should be in filter-checkbox class with filter data
        )
      ).map(function (ele) {
        // map function to apply changes on arry
        return ele.value; // value  of imput tag                      // from tag only tag value save in array
      });
    });
    console.log(filter_object);

    $.ajax({
      url: "/filter_product",
      data: filter_object,
      dataType: "json",
      beforeSend: function () {
        console.log("sending data...");
      },
      success: function (response) {
        console.log(response);
        console.log("task compleated successfully");
        $("#filtered_product").html(response.data);
      },
    });
  });

  $("#max_price1").on("blur", function () {
    let min_price = $(this).attr("min");
    let max_price = $(this).attr("max");
    let current_price = $(this).val();

    console.log("crurent price is: ", current_price);
    console.log("min price is: ", min_price);
    console.log("max price is: ", max_price);

    if (
      current_price > parseInt(max_price) ||
      current_price < parseInt(min_price)
    ) {
      alert("Price Must be Between " + min_price + " and " + max_price);
      $(this).val(min_price);
      $("#range").val(min_price);

      $(this).focus();
      console.log("Error");

      return false;
    }

    // $.ajax({
    //   url: "/filter_product",
    //   data: {
    //     max_price: max_price,
    //   },
    //   dataType: "json",
    //   success: function (response) {
    //     console.log(response);
    //     console.log("task completed successfully");
    //     $("#filtered_product").html(response.data);
    //   },
    // });
  });

  //add to cart actual
  $(".add-to-cart-btn").on("click", function () {
    console.log("Add to cart clicked");

    let current_button = $(this);
    let index = current_button.attr("data-index");
    let product_id = $(".product-id-" + index).val();
    let quantity = $(".product-qty-" + index).val();
    let product_title = $(".product-title-" + index).val();
    let product_price = $(".product-price-" + index).text();
    let product_pid = $(".product-pid-" + index).val();
    let product_image = $(".product-image-" + index).val();

    console.log(product_id);
    console.log(quantity);
    console.log(product_title);
    console.log(product_price);
    console.log(product_pid);
    console.log(product_image);

    $.ajax({
      url: "/add_to_cart",
      data: {
        id: product_id,
        pid: product_pid,
        image: product_image,
        qty: quantity,
        title: product_title,
        price: product_price,
      },
      dataType: "json",
      beforeSend: function () {
        console.log("Adding Product to cart...");
      },
      success: function (res) {
        console.log("task completed successfully");
        console.log(res.total);
        current_button.html("<span>&#10003;</span>");
        console.log(res);

        $(".cart_count").text(res.total);
        $(".cart_total_price").text(res.totalsum);
      },
    });
  });

  $(document).on("click", ".delete_product", function () {
    let product_id = $(this).attr("data_prodct");

    console.log(product_id);
    var jq = jQuery.noConflict(); //jquery 1.11 and 3.1 conflict $ sign and it doesnt work

    jq.ajax({
      url: "/delete-from-cart",
      data: {
        id: product_id,
      },
      dataType: "json",
      beforeSend: function () {
        $(this).hide();
      },
      success: function (response) {
        $(this).show();
        $(".cart_total_price").text(response.totalsum);
        $(".cart_count").text(response.total);
        $("#cart-list").html(response.data);
      },
    });
  });

  //
  // Use delegated event binding:
  $(document).on("click", ".update_product", function () {
    // let product_id = $(".product_id").attr("data-index");
    // let product_qty = $(".product-qty-" + product_id).val();

    // console.log(product_id);

    let products = {};

    // Iterate over all products in the cart and collect their IDs and quantities
    $(".product-row").each(function () {
      let product_id = $(this).find(".product_id").attr("data-index"); // Get product ID find product_id class in this template
      let product_qty = $(this)
        .find(".product-qty-" + product_id)
        .val(); // Get product quantity // Get product ID

      // Add to the products object
      console.log(product_id);
      console.log(product_qty);
      products[product_id] = product_qty;
    });

    console.log(products);
    var jq = jQuery.noConflict(); //jquery 1.11 and 3.1 conflict $ sign and it doesnt work Reason for views not wrking but js does
    jq.ajax({
      url: "/update_from_cart/",
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken, // Add the CSRF token here
      },
      data: {
        products: JSON.stringify(products),
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(), // Add CSRF token for security
      },
      dataType: "json",
      beforeSend: function () {
        $(this).hide();
        console.log("working ");
      },
      success: function (response) {
        $(this).show();
        $(".cart_total_price").text(response.totalsum);
        $(".cart_count").text(response.total);
        $("#cart-list").html(response.data);
      },
    });
  });

  // make default address
  $(document).on("click", ".make-default-address", function () {
    let id = $(this).attr("data-address-id");
    let this_val = $(this);

    console.log(id);

    $.ajax({
      url: "/make_default_address",
      data: {
        id: id,
      },
      dataType: "json",
      success: function (res) {
        console.log("address is added");
        if (res.boolean == true) {
          $(".check").hide();
          $(".action_btn").show();

          $(".check" + id).show();
          $(".button" + id).hide();
        }
      },
    });
  });
});
// Add to cart bassed on session and session data
// $("#add-to-cart-btn").on("click", function () {
//   console.log("Add to cart clicked");

//   let product_id = $(".product_id").val();
//   let quantity = $(".quantity").val();
//   let product_title = $(".product_title").val();
//   let product_price = $(".product_price").text();
//   let current_button = $(this);

//   console.log(product_id);
//   console.log(quantity);
//   console.log(product_title);
//   console.log(product_price);

//   $.ajax({
//     url: "/add_to_cart",
//     data: {
//       id: product_id,
//       qty: quantity,
//       title: product_title,
//       price: product_price,
//     },
//     dataType: "json",
//     beforeSend: function () {
//       console.log("Adding Product to cart...");
//     },
//     success: function (res) {
//       console.log("task completed successfully");
//       console.log(res.total);
//       current_button.html("Added to cart");
//       console.log(res);

//       $(".cart_count").text(res.total);
//       $(".cart_total_price").text(res.totalsum);
//     },
//   });
// });
