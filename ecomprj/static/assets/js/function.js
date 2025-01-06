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
});

// Add to cart
$("#add-to-cart-btn").on("click", function () {
  console.log("Add to cart clicked");

  let product_id = $(".product_id").val();
  let quantity = $(".quantity").val();
  let product_title = $(".product_title").val();
  let product_price = $(".product_price").text();
  let current_button = $(this);

  console.log(product_id);
  console.log(quantity);
  console.log(product_title);
  console.log(product_price);

  $.ajax({
    url: "/add_to_cart",
    data: {
      id: product_id,
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
      current_button.html("Added to cart");
      console.log(res);

      $(".cart_count").text(res.total);
      $(".cart_total_price").text(res.totalsum);
    },
  });
});
