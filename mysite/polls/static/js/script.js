window.addEventListener("DOMContentLoaded", () => {
  const submitButton = document.getElementById("button_submit");
  const addInputsButton = document.getElementById("button_add_inputs");

  submitButton.addEventListener("click", uploadFiles);
  addInputsButton.addEventListener("click", addInputs);

  function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
  }

  function addInputs() {
    for (let i = 1; i <= 2; i++) {
      const input = document.createElement("input");
      input.setAttribute("class", `col_file_${i}`);
      input.setAttribute("type", `text`);
      input.placeholder = "Digite a coluna";

      const inputContainer = document.getElementById(
        `file_${i}_inputs`
      ).lastElementChild;
      insertAfter(inputContainer, input);
    }
  }

  function getAllInputs() {
    const columns = [];

    for (let i = 1; i <= 2; i++) {
      const inputValuesArray = [];
      const inputs = document.querySelectorAll(`input.col_file_${i}`);

      inputs.forEach((input) => {
        inputValuesArray.push(input.value);
      });

      columns.push(inputValuesArray);
    }

    return columns;
  }

  function uploadFiles() {
    const file1 = document.getElementById("file_1").value;
    const file2 = document.getElementById("file_2").value;

    if (file1 && file2) {
      const form = document.getElementById("uploadForm");
      const formData = new FormData(form);

      const lastInput =
        document.getElementById("file_1_inputs").firstElementChild;

      formData.append(
        "columns",
        lastInput.value.length > 0 ? getAllInputs() : []
      );

      fetch("get_sheets", {
        method: "post",
        body: formData,
      })
        .then((response) => /* response.blob() */ console.log(response.data))
        // .then((blob) => {
        //   const fileUrl = window.URL.createObjectURL(blob);
        //   const downloadLink = document.getElementById("downloadLink");
        //   const fileLink = document.getElementById("fileLink");

        //   fileLink.href = fileUrl;
        //   downloadLink.style.display = "block";
        // })
        .catch((error) => {
          console.error("Erro ao enviar o arquivo:", error);
        });
    }
  }
});
