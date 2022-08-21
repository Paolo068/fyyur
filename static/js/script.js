window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

// Confirm delete

// delBtn = document.querySelector('#to-delete')
// if (delBtn) {
//   delBtn.addEventListener('click', e => {
//     if (!confirm('Are you sure to delete?')) {
//       e.preventDefault()
//     }
//     else {
//       return null
//     }
//   })
// }






