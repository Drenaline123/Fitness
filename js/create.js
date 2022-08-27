
var workouts = {{workouts}};
var image = {{images}};
var video = {{videos}};
var i = 0
var table = document.getElementById("table");
document.getElementById("search").addEventListener("input", (e) => {
    let value = e.target.value
    if (value && value.trim().length >0){
        value = value.trim().toLowercase()
    }
    else {
        error = "invalid input"
    }
})
function renderlist(){
    for (item in workouts){
        if (item.contains(search.value)){
            table.rows[i].cells[1].innerHTML = workouts[i]
            document.getElementById('image${i}').src = "${image(item.index)}.jpeg"
            document.getElementById('video${i}').src = "https://www.youtube.com/embed/${video(item.index)}?autoplay=1"
            i++
        }
    }

}
renderlist()