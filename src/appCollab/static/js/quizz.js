/* Response is checked 
    return list: name of input checked
*/
function isChecked(){
    let checkedBox = []; 
    const inputElements = document.getElementsByClassName('reponse');
    for(var i=0; i < inputElements.length; ++i){
        if(inputElements[i].checked){
            checkedBox.push(inputElements[i].getAttribute("name"));
        }
    }
    return checkedBox
}

/* Add Leading Zeros
- num(int)        : value where zeros will be added
- totalLength(int): number of zeros that will be added
return str        : value with totalLength zeros added  
*/
function addLeadingZeros(num, totalLength) {
    return String(num).padStart(totalLength, '0');
}



/* Add data in tag
*/
const containerRep  = document.getElementById("container-reponses");
function updateTag(){
    document.getElementById("titre").textContent    = addLeadingZeros(numQuestion+1, 2) + "/" + (totalQ) + " - " + titre; // title
    document.getElementById("intitule").textContent = intitule                                                          // entitled
    // Responses
    containerRep.innerHTML = ""; // empty the div of its children to add the new answers whose number of answers can be more 
                                 //   or less than the answers of the previous question
    const tagsRep = document.createElement("div");
    for (let r = 0; r < listRep.length; r++) {
        tagsRep.innerHTML  += `<input name=${r+1} type="checkbox" class="reponse">
                               <label for=${r+1} class="labRep"> ${listRep[r]} </label> `;
      } 
      containerRep.appendChild(tagsRep);

} 

window.onload = function() {
    updateTag()
  };
  