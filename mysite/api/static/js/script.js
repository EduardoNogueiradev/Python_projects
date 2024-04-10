window.addEventListener("DOMContentLoaded", () => {
  const submitButton = document.getElementById("buttonSubmit");
  const addInputsButton = document.getElementById("buttonAddInputs");
  const dropdownButton = document.getElementById("buttonDropdown");

  dropdownButton.addEventListener("click", changeDropdownVisibility);
  submitButton.addEventListener("click", uploadFiles);
  addInputsButton.addEventListener("click", addInputs);

  const fileArea1 = document.getElementById("fileArea1");
  const fileArea2 = document.getElementById("fileArea2");

  const file1 = document.getElementById("file1");
  const file2 = document.getElementById("file2");

  const fileContent1 = document.getElementById("fileContent1");
  const fileContent2 = document.getElementById("fileContent2");

  fileArea1.addEventListener("click", () => {
    file1.click();
  });
  fileArea2.addEventListener("click", () => {
    file2.click();
  });

  file1.addEventListener("change", () => {
    if (file1.value.length > 0) {
      fileArea1.classList.add("file-filled");
      value = file1.value.replace("C:\\fakepath\\", "");
      fileContent1.innerHTML = value;
    }
  });
  file2.addEventListener("change", () => {
    if (file2.value.length > 0) {
      fileArea2.classList.add("file-filled");
      value = file2.value.replace("C:\\fakepath\\", "");
      fileContent2.innerHTML = value;
    }
  });

  function changeDropdownVisibility() {
    const dropdown = document.getElementById("dropdown");
    dropdown.classList.toggle("show-dropdown");
  }

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
    if (file1.value && file2.value) {
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
    } else {
      alert("Preencha todos os campos!");
    }
  }
});
