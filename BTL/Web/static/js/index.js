function addToCart(id, name, price) {
    event.preventDefault()
    // promise
    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)

        let counter = document.getElementById('cartCounter')
        counter.innerText = data.total_quantity
    }).catch(function(err) {
        console.error(err)
    })
}

//function pay() {
//    if (confirm('Ban chac chan muon thanh toan khong?') == true) {
//        fetch('/api/pay', {
//            method: 'post'
//        }).then(res => res.json()).then(data => {
//            if (data.code == 200)
//                location.reload()
//        }).catch(err =>  console.error(err))
//    }
//}
function addToMedicalForm(id, name) {
    event.preventDefault()
    // promise
    fetch('/api/add-form', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)

        let counter = document.getElementById('Counter')
        counter.innerText = data.total_quantity
    }).catch(function(err) {
        console.error(err)
    })
}

function delete_cart(id){
    if (confirm('Ban chac chan muon thanh toan khong?') == true) {
        fetch('/api/delete-cart/' + id, {
        method: 'delete',
        headers: {
            'Content-Type': 'application/json'
        }
        }).then(function(res) {
            console.info(res)
            return res.json()
        }).then(function(data) {
            console.info(data)
            let counter = document.getElementById('cartCounter')
            counter.innerText = data.total_quantity
            let e = document.getElementById('medicine'+id)
            e.style.display = 'none'
            location.reload()
        }).catch(function(err) {
            console.error(err)
        })
    }
}

function delete_form(id){
    if (confirm('Ban chac chan muon thanh toan khong?') == true) {
        fetch('/api/delete-form/' + id, {
        method: 'delete',
        headers: {
            'Content-Type': 'application/json'
        }
        }).then(function(res) {
            console.info(res)
            return res.json()
        }).then(function(data) {
            console.info(data)
            let counter = document.getElementById('Counter')
            counter.innerText = data.total_quantity
            let e = document.getElementById('medicine'+id)
            e.style.display = 'none'
            location.reload()
        }).catch(function(err) {
            console.error(err)
        })
    }
}
function add() {
    if (confirm('Ban chac chan muon thanh toan khong?') == true) {
        fetch('/api/pay', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code == 200)
                location.reload()
        }).catch(err =>  console.error(err))
    }
}
$(document).ready(function(){
        $('#search1').hide();
        $('#search').click(function(){
            $('#search1').toggle();
        });
        $('.tab-main .tab-title').first().addClass("active");
        $('.content').hide();
        $('.tab-main .tab-content .content').first().show();
        $('.tab-main .tab-title').hover(function () {
            $(this).siblings().removeClass("active");
            $(this).addClass("active");
            $(this).css('transition-duration', '0.9s');
            var tab = $(this).index();
            $('.content').hide();
            $('.content').eq(tab).show();
    });
});
function ExportToExcel(type, id, fn, dl) {
       var elt = document.getElementById(id);
       var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
       return dl ?
         XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
         XLSX.writeFile(wb, fn || ('MySheetName.' + (type || 'xlsx')));
    }
