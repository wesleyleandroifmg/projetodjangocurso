let tamanhoFonte = 100;

function aplicarFonte() {
  document.documentElement.style.fontSize = tamanhoFonte + "%";
}

function aumentarFonte() {
  if (tamanhoFonte < 140) {
    tamanhoFonte += 10;
    aplicarFonte();
    salvarPreferencias();
  }
}

function diminuirFonte() {
  if (tamanhoFonte > 80) {
    tamanhoFonte -= 10;
    aplicarFonte();
    salvarPreferencias();
  }
}

function alternarContraste() {
  document.body.classList.toggle("alto-contraste");
  salvarPreferencias();
}

function resetarAcessibilidade() {
  tamanhoFonte = 100;
  aplicarFonte();

  document.body.classList.remove("alto-contraste");

  localStorage.removeItem("acessibilidade");

  anunciarLeitorDeTela("Configurações de acessibilidade resetadas");
}

/* =========================
   ACESSIBILIDADE EXTRA
========================= */

function anunciarLeitorDeTela(mensagem) {
  let liveRegion = document.getElementById("aria-live");

  if (!liveRegion) {
    liveRegion = document.createElement("div");
    liveRegion.id = "aria-live";
    liveRegion.setAttribute("aria-live", "polite");
    liveRegion.className = "visually-hidden";
    document.body.appendChild(liveRegion);
  }

  liveRegion.textContent = mensagem;
}

/* =========================
   SALVAR PREFERÊNCIAS
========================= */

function salvarPreferencias() {
  const preferencias = {
    fonte: tamanhoFonte,
    contraste: document.body.classList.contains("alto-contraste")
  };

  localStorage.setItem("acessibilidade", JSON.stringify(preferencias));
}

function carregarPreferencias() {
  const dados = localStorage.getItem("acessibilidade");

  if (!dados) return;

  const preferencias = JSON.parse(dados);

  tamanhoFonte = preferencias.fonte || 100;
  aplicarFonte();

  if (preferencias.contraste) {
    document.body.classList.add("alto-contraste");
  }
}

document.addEventListener("DOMContentLoaded", carregarPreferencias);