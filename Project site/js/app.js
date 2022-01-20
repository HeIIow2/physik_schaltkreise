const root = document.documentElement;
const header = document.getElementsByTagName("header")[0];

let theme;

var theme_str = getCookie("theme");
if (theme_str == "") {
	theme = 0;
	setCookie("theme", 0, 9999999);
} else {
	theme = parseInt(theme_str);
}

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

set_theme(theme)

function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function set_theme(theme_) {
	for (var i=0; i<properties.length; i++) {
		const propertie = properties[i]
		root.style.setProperty(propertie, colors[propertie][theme_]);
	}
}

function toggle() {
	theme += 1;
	theme = theme % colors[properties[0]].length;
	
	set_theme(theme);
	setCookie("theme", theme, 9999999);
}
