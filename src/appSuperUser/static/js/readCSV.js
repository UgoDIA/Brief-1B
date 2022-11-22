const csvFile = document.getElementById('csvFile')
const form = document.getElementById('myForm')

// Extract data from csv 
csvFile.addEventListener('change', (e) => {
    Papa.parse(csvFile.files[0], {
        download: true,
        encoding: "ISO-8859-1",
        header: false,
        skipEmptyLines: true,
        complete: function(results){
            fillHtmlTable(results.data)
        }
    })
})

// Fill table with data
function fillHtmlTable(res){
    const table = document.getElementById("data_table");
    emptyTable(table)
    let table_len = (table.rows.length) - 1;
    for (let i = 1; i < res.length; i++) { 
        table.insertRow(table_len).outerHTML = "<tr id='row"+table_len+"'><td id='name_row"+table_len+"'>"+res[i][7]+"</td><td id='country_row"+table_len+"'>"+res[i][6]+"</td><td id='age_row"+table_len+"'>"+res[i][5]+"</td><td id='pwd_row" + table_len + "'>" + res[i][5] + "</td><td><input type='button' id='edit_button"+table_len+"' value='Edit' class='edit' onclick='edit_row("+table_len+")'> <input type='button' id='save_button"+table_len+"' value='Save' class='save' onclick='save_row("+table_len+")' style='display:none'> <input type='button' value='Delete' class='delete' onclick='delete_row("+table_len+")'></td></tr>";
        table_len += 1;
  }
}

// Empty the table
function emptyTable(table){
    table.innerHTML = `
    <div id="wrapper">
    <table align='center' cellspacing=2 cellpadding=5 id="data_table" border=1>
       <tr>
          <th>Prénom</th>
          <th>Nom</th>
          <th>Matricule</th>
          <th>Password</th>
       </tr>
       <tr>
          <td> <input type="text" id="new_name">    </td>
          <td> <input type="text" id="new_country"> </td>
          <td> <input type="text" id="new_age">     </td>
          <td> <input type="text" id="new_pwd">     </td>
          <td> <input type="button" class="add" onclick="add_row();" value="Add Row"></td>
       </tr>
    </table>
 </div>`
}

// Get Data from html table
function getDataFromTable(){
    const table = document.getElementById("data_table")
    let dict = {};
    for (let e = 1; e < table.rows.length -1; e++) { // car on ne veut pas la pour le header et la ligne qui permet d'ajouter un élément
        table.rows[e].cells[0].innerText
        dict[e] = {"prenom"   : table.rows[e].cells[0].innerText, 
                   "nom"      : table.rows[e].cells[1].innerText, 
                   "matricule": table.rows[e].cells[2].innerText, 
                   "password" : table.rows[e].cells[3].innerText}
    }
    return dict
}

function sendData(event){
    event.preventDefault();
    console.log("sendData")
    const res = getDataFromTable()
    // console.log(res)
    const csrf  = $('input[name="csrfmiddlewaretoken"]').val()  
    $.ajax({
        type: "POST",
        url: 'addDataInDB',
        data: {
            csrfmiddlewaretoken : csrf,
            "result": res//[{"val1": 1, "val2":2}, {"val1": 3, "val2":4}] //res,
        },
        dataType: "json",
        success: function (data) {
            // any process in data
            alert("successfull")
        },
        failure: function () {
            alert("failure");
        }
    })
}

form.addEventListener('submit', sendData);
