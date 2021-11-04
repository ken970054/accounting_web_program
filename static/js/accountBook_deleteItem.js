
$(document).ready(function() {
    
    // read delete item's date and time and post to flask.
    $("#accountBook_table").on('click','.deleteButton',function() {

        //confirm this delete movement
        var popup_message = confirm("Are you sure you want to delete this record?")
        if (popup_message) {
            // get the current row
            var currentRow = $(this).closest("tr"); 
            
            var record_type = currentRow.find("th").text(); // get type data
            recordCount_delete = currentRow.find("td:eq(9)").text();
            
            
            var record_datetime = currentRow.find("td:eq(6)").text(); // get date time value
            var datetimeArr = record_datetime.split(" "); // split date and time
            
            // store in directionary form
            const form = {
                deleteButton_book: true,
                transType: record_type,
                recordCount: recordCount_delete,
                recordDate: datetimeArr[0],
                recordTime: datetimeArr[1]
            };
            
            const path = '/account/book';
            axios.post(path, form, axiosConfig)
                .then(res => {
                    console.log('[完成delete_item_datetime傳遞]', form);
                    window.location.reload();
                })
                .catch(err => {
                    console.log('[傳遞delete_item_datetime失敗]', err);
                });
        }
    });
});