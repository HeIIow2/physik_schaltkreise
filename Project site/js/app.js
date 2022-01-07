const root = document.documentElement;
const header = document.getElementsByTagName("header")[0];
console.log(header);

let theme = 0;
function toggle() {
	console.log("toggle");
	const colors = {
		"--bg-color": ["#121212", "#fff"],
		"--bg-1dp": ["#1e1e1e", "#f2f2f2"],
		"--bg-2dp": ["rgba(255, 255, 255, 0.07)", "rgba(0, 0, 0, 0.07)"],
		"--bg-3dp": ["rgba(255, 255, 255, 0.08)", "rgba(0, 0, 0, 0.08)"],
		"--bg-4dp": ["rgba(255, 255, 255, 0.09)", "rgba(0, 0, 0, 0.09)"],
	
		"--main-text-color": ["#fff", "#000"],
		"--secondary-text-color": ["#aaa", "#333"],
	
		"--accent-color": ["#5b8c80", "#5b8c80"],
		"--shadow-1dp": ["0 0 10px black", "0 0 0 2px var(--accent-color)"],
		"--shadow-2dp": ["0 0 20px black", "0 0 0 2px var(--accent-color)"]
	}
	const properties = Object.keys(colors);
	theme += 1;
	theme = theme % colors[properties[0]].length;
	
	for (var i=0; i<properties.length; i++) {
		const propertie = properties[i]
		root.style.setProperty(propertie, colors[propertie][theme]);
	}
}
