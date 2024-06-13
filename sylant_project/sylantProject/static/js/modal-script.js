document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('deleteModal');
    var span = document.getElementsByClassName('close')[0];
    var cancelBtn = document.getElementsByClassName('btn-cancel')[0];
    var deleteBtn = document.getElementById('btn-delete');

    deleteBtn.onclick = function() {
        var id = this.getAttribute('data-id');
        var name = this.getAttribute('data-name');
        var url = this.getAttribute('data-url');
        document.getElementById('modal-machine-name').textContent = name;
        document.getElementById('deleteForm').action = url;
        modal.style.display = 'block';
    };

    span.onclick = function() {
        modal.style.display = 'none';
    };

    cancelBtn.onclick = function() {
        modal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };
});