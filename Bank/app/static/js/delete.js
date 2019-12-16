function sure(){
    if(confirm('Sure to delete?'))
    {
        this.document.delete.submit();
        return true;
    }
}
