
function getLocalTime(nS) {  
	if (nS == 0)
		{
			return '';
		}
	else if (nS == 'None')
		return '';
	else
		{
			return new Date(parseInt(nS) * 1000).toLocaleString().replace(/:\d{1,2}$/,' ');  
		}
} 

function convertMySQLDate(ns){
	// Split timestamp into [ Y, M, D, h, m, s ]
	var t = ns.split(/[- :]/);

	// Apply each element to the Date function
	var d = new Date(t[0], t[1]-1, t[2], t[3], t[4], t[5]);

	//alert(d);	
	return d
}

function convertStatus(localStatus)
{
	switch(localStatus)
	{
		case 11:
			return '可借';
		case 12:
			return '已借';
		case 13:
			return '不可借';
		default:
			return '状态出错';
	}
}

function borrowLink(currentStatus)
{
	switch(currentStatus)
	{
		case 0:
		case 1:
		case 3:
			return true;
		case 2:
			return false;
	}
}

function backLink(currentStatus)
{
	switch(currentStatus)
	{
		case 2:
			return true;
		default:
			return false
	}
}