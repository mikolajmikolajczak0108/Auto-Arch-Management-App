// Fetch data from the Django view
fetch('/director/statistics/', {
    headers: {
        'X-Requested-With': 'XMLHttpRequest'  // Indicate AJAX request
    }
})
.then(response => response.json())
.then(data => {
    // Parse JSON data
    const ongoingProjectsData = JSON.parse(data.ongoing_projects);
    const projectFilesData = JSON.parse(data.project_files);
    const completedProjectsTimeData = JSON.parse(data.completed_projects_time);
    const investorProjectsData = JSON.parse(data.investor_projects);

    // Function to create animated charts
    function createAnimatedChart(ctx, type, labels, data, label) {
        return new Chart(ctx, {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuad'
                }
            }
        });
    }



// Create an empty object to store the count of projects for each month
let monthlyProjectCounts = {};

// Loop through each project to count the number of projects for each month
ongoingProjectsData.forEach(project => {
    const startDate = new Date(project.start_date);
    const endDate = new Date(project.end_date);
    let currentDate = new Date(startDate);

    while (currentDate <= endDate) {
        const monthYear = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}`;

        // Increment the count for this month
        if (monthlyProjectCounts[monthYear]) {
            monthlyProjectCounts[monthYear]++;
        } else {
            monthlyProjectCounts[monthYear] = 1;
        }

        // Move to the next month
        currentDate.setMonth(currentDate.getMonth() + 1);
    }
});

// Generate the last 12 months for the x-axis
const last12Months = Array.from({ length: 12 }, (_, i) => {
    const d = new Date();
    d.setMonth(d.getMonth() - i);
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
}).reverse();

// Generate the project counts for the last 12 months
const last12MonthsCounts = last12Months.map(monthYear => monthlyProjectCounts[monthYear] || 0);

// Creating the line chart
createAnimatedChart(
    document.getElementById('ongoingProjectsChart').getContext('2d'),
    'line',
    last12Months,
    last12MonthsCounts,
    'Projekty w toku'
);

// Parsing the JSON string from the Django backend to get the projects data
const projectsData = JSON.parse(data.user_projects);

// Create an empty object to store the count of projects for each user
let userProjectCounts = {};

// Loop through each project to count the number of projects for each user
projectsData.forEach(project => {
    // Assuming each project object has a 'user_id' field that indicates the user associated with the project
    let username = project.username;  // Replace 'user_id' with the actual field name if it's different

    // Increment the count for this user
    if (userProjectCounts[username]) {
        userProjectCounts[username]++;
    } else {
        userProjectCounts[username] = 1;
    }
});

// Extract the user IDs and their respective project counts for the chart
let userIDs = Object.keys(userProjectCounts);
let projectCounts = Object.values(userProjectCounts);

// Creating the bar chart
let userProjectsChart = createAnimatedChart(
    document.getElementById('userProjectsChart').getContext('2d'),
    'bar',
    userIDs,
    projectCounts,
    'Projekty pracowników'
);

// Create an object to hold the sum of file counts for each project
const projectFileCounts = {};

// Loop through the data to sum up the file counts for each project
projectFilesData.forEach(item => {
    if (projectFileCounts[item.project_name]) {
        projectFileCounts[item.project_name] += item.count;
    } else {
        projectFileCounts[item.project_name] = item.count;
    }
});

// Extract the unique project names and their summed file counts
const projectNames = Object.keys(projectFileCounts);
const fileCounts = Object.values(projectFileCounts);

// Create the animated chart
createAnimatedChart(
    document.getElementById('projectFilesChart').getContext('2d'),
    'bar',
    projectNames,  // X-axis labels
    fileCounts,    // Y-axis data
    'Projekty wg. ilości plików' // Chart title
);


// Projects for Each Investor
const investorList = document.getElementById('investorProjectsList');

// Sort the investors by the number of projects in descending order
investorProjectsData.sort((a, b) => b.count - a.count).forEach(investor => {
    const listItem = document.createElement('div');
    listItem.textContent = `Inwestor: ${investor.investor_name} Liczba projektów: ${investor.count}`;
    investorList.appendChild(listItem);
});

    // Toggle Investor List
    document.getElementById('toggleInvestorList').addEventListener('click', function() {
        const investorList = document.getElementById('investorProjectsList');
        investorList.classList.toggle('show');
    });
});
