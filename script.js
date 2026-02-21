document.getElementById("generate").addEventListener("click", async () => {
    const skill = document.getElementById("skill").value;
    const level = document.getElementById("level").value;
    const semesters = document.getElementById("semesters").value;
    const weekly_hours = document.getElementById("weekly_hours").value;
    const industry_focus = document.getElementById("industry_focus").value;
  
    const response = await fetch("http://127.0.0.1:5000/api/generate-curriculum", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ skill, level, semesters, weekly_hours, industry_focus })
    });
  
    const data = await response.json();
    console.log(data);
    displayCurriculum(data);
  });
  
  function displayCurriculum(data) {
    const section = document.getElementById("output-section");
    const container = document.getElementById("curriculum-display");
    container.innerHTML = "";
  
    if (data.curriculum) {
      section.classList.remove("hidden");
      data.curriculum.forEach((sem) => {
        const sDiv = document.createElement("div");
        sDiv.innerHTML = `<h3>Semester ${sem.semester}</h3>`;
        sem.courses.forEach((c) => {
          const card = document.createElement("div");
          card.className = "course-card";
          card.innerHTML = `<h4>${c.name} (${c.credits} credits)</h4><ul>${c.topics.map(t => `<li>${t}</li>`).join("")}</ul>`;
          sDiv.appendChild(card);
        });
        container.appendChild(sDiv);
      });
    }
  }
  
  document.getElementById("download-pdf").addEventListener("click", async () => {
    const skill = document.getElementById("skill").value;
    const container = document.getElementById("curriculum-display");
  
    if (!container.innerHTML.trim()) return alert("No curriculum found!");
    const data = {
      program_name: `${skill} Curriculum`,
      curriculum: JSON.parse(localStorage.getItem("curriculum_data")) || []
    };
  
    const res = await fetch("http://127.0.0.1:5000/api/download-pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
  
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${skill}_Curriculum.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  });
  