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
    // var columns = [];

    // for (let i = 1; i <= 2; i++) {
    //   const inputValuesArray = [];
    //   const inputs = document.querySelectorAll(`input.col_file_${i}`);

    //   inputs.forEach((input) => {
    //     inputValuesArray.push(input.value);
    //   });

    //   columns.push(inputValuesArray);
    // }

    var columns = [
      ["nota", "cfop", "fantasiacliente", "valortotal"],
      ["nota", "cfop", "cliente", "valor contabil"],
    ];

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
        .then((response) => {
          if (!response.ok) {
            throw new Error("Erro ao receber o arquivo");
          }

          return response.blob();
        })
        .then((blob) => {
          const url = window.URL.createObjectURL(blob);

          const fileLink = document.createElement("a");
          fileLink.href = url;
          fileLink.download = "compared_sheets.xlsx";

          document.body.appendChild(fileLink);
          fileLink.click();

          document.body.removeChild(fileLink);
          window.URL.revokeObjectURL(url);
        })
        .catch((error) => {
          console.error("Erro: ", error);
        });
    }
  }
});
