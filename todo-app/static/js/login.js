document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const resetForm = document.getElementById("reset-form");

  const goToRegister = document.getElementById("go-to-register");
  const goToLogin = document.getElementById("go-to-login");
  const goToReset = document.getElementById("go-to-reset");
  const backToLogin = document.getElementById("back-to-login");

  // Gestion des affichages des formulaires
  goToRegister.addEventListener("click", () => {
    loginForm.classList.remove("active");
    registerForm.classList.add("active");
    resetForm.classList.remove("active");
  });

  goToLogin.addEventListener("click", () => {
    loginForm.classList.add("active");
    registerForm.classList.remove("active");
    resetForm.classList.remove("active");
  });

  goToReset.addEventListener("click", () => {
    loginForm.classList.remove("active");
    registerForm.classList.remove("active");
    resetForm.classList.add("active");
  });

  backToLogin.addEventListener("click", () => {
    loginForm.classList.add("active");
    registerForm.classList.remove("active");
    resetForm.classList.remove("active");
  });

  // Enregistrement des utilisateurs
  registerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = document.getElementById("register-name").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    if (email && password) {
      localStorage.setItem(email, JSON.stringify({ name, email, password }));
      alert("Inscription réussie ! Vous pouvez maintenant vous connecter.");
      registerForm.reset();
      goToLogin.click();
    } else {
      alert("Veuillez remplir tous les champs.");
    }
  });

  // Connexion des utilisateurs
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const user = localStorage.getItem(email);
    if (user) {
      const userData = JSON.parse(user);
      if (userData.password === password) {
        alert('Bienvenue,  ${userData.name} !');
        localStorage.setItem('"currentUser", email');
        window.location.href = "liste.html";
      } else {
        alert("Mot de passe incorrect.");
      }
    } else {
      alert("Aucun compte trouvé avec cet email.");
    }
  });
});