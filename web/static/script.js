/*

made by lilyscripts
https://discord.gg/S4NHgEVmxy

*/

const form = $(".form");
const result = $(".result");
const refresh = $(".refresh");
const copy_cookie = $(".copy");
const retry = $(".retry");
const cookie = $(".cookie");
const refreshed_cookie = $(".refreshed_cookie");
const discord = $(".discord");
const credits = $(".credits");

refresh.on("click", () => {
	$.post("refresh", {
		cookie: cookie.val(),
	})
		.done((data) => {
			let error = data.error;
			let cookie = data.cookie;
			let message = data.message;

			form.hide();
			result.show();
			retry.show();
			refreshed_cookie.show();

			if (error) {
				refreshed_cookie.css("line-height", "200px");
				refreshed_cookie.val(message);
				return;
			}

			copy_cookie.show();
			refreshed_cookie.val(cookie);
		})
		.fail((xhr) => {
			if (xhr.status === 429) {
				alert("you are ratelimited, please wait and try again");
			} else {
				alert("an unknown error occurred");
			}
		});
});

copy_cookie.on("click", () => {
	navigator.clipboard.writeText(refreshed_cookie.val());
	alert("copied refreshed cookie to clipboard");
});

retry.on("click", () => {
	window.location.reload();
});

discord.on("click", () => {
	window.open("https://discord.gg/S4NHgEVmxy", "_BLANK");
});

credits.on("click", () => {
	window.open("https://github.com/lilyscripts/cookie-refresher", "_BLANK");
});
