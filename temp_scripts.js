    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Gunnar Hostetler",
        "url": "https://gunnarguy.me/",
        "jobTitle": "Healthcare Operations Specialist & AI Developer",
        "email": "Gunnarguy@me.com",
        "telephone": "+14088280552",
        "address": {
          "@type": "PostalAddress",
          "addressLocality": "Campbell",
          "addressRegion": "CA"
        },
        "sameAs": [
          "https://www.linkedin.com/in/gunnar-hostetler/",
          "https://github.com/Gunnarguy"
        ]
      }
    </script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-YZ95J7YFJV"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {
            dataLayer.push(arguments);
        }
        gtag("js", new Date());
        gtag("config", "G-YZ95J7YFJV");
    </script>
    <script>
        // Mobile navigation toggle
        const navToggle = document.querySelector(".nav-toggle");
        const navMenu = document.querySelector(".nav-menu");

        if (navToggle && navMenu) {
            navToggle.addEventListener("click", () => {
                const isOpen = navMenu.classList.toggle("nav-menu-active");
                navToggle.classList.toggle("nav-toggle-active");
                navToggle.setAttribute("aria-expanded", isOpen);
        });
      }

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
            anchor.addEventListener("click", function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute("href"));
                if (target) {
                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start",
            });
              // Close mobile menu if open
              if (navMenu) navMenu.classList.remove("nav-menu-active");
              if (navToggle) navToggle.classList.remove("nav-toggle-active");
          }
        });
      });

        // Enhanced form submission handler
        const contactForm = document.querySelector("form");
        if (contactForm) {
            contactForm.addEventListener("submit", function (e) {
                e.preventDefault();

            // Get form data
            const formData = new FormData(this);
            const name = formData.get("name");
            const email = formData.get("email");
            const subject = formData.get("subject");
            const message = formData.get("message");

            // Basic validation
            if (!name || !email || !subject || !message) {
                alert("Please fill in all fields.");
                return;
          }

            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert("Please enter a valid email address.");
                return;
          }

            // Open mailto link with form data
            const mailtoLink = `mailto:Gunnarguy@me.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(`From: ${name} (${email})\n\n${message}`)}`;
            window.location.href = mailtoLink;
            this.reset();
        });
      }

        // Scroll-based navigation highlighting
        window.addEventListener("scroll", () => {
            const sections = document.querySelectorAll("section[id]");
            const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');

          let current = "";
          sections.forEach((section) => {
              const sectionTop = section.offsetTop;
              const sectionHeight = section.clientHeight;
              if (window.pageYOffset >= sectionTop - 200) {
                  current = section.getAttribute("id");
              }
        });

          navLinks.forEach((link) => {
              link.classList.remove("active");
              if (link.getAttribute("href") === `#${current}`) {
                  link.classList.add("active");
              }
          });
      });

        // Add loading animation for project images
        document.querySelectorAll(".project-image img").forEach((img) => {
            img.addEventListener("load", function () {
                this.style.opacity = "1";
            });
            img.addEventListener("error", function () {
                if (!this.dataset.fallback) {
                    this.dataset.fallback = "true";
                    this.src =
                        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='250' fill='%23f0f0f0'%3E%3Crect width='400' height='250'/%3E%3Ctext x='50%25' y='50%25' fill='%23999' font-family='sans-serif' font-size='16' text-anchor='middle' dy='.3em'%3EProject Image%3C/text%3E%3C/svg%3E";
                }
        });
      });

        // Add animation on scroll for elements
        const observerOptions = {
            threshold: 0.1,
            rootMargin: "0px 0px -50px 0px",
      };

        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("animate-in");
                    obs.unobserve(entry.target);
          }
        });
      }, observerOptions);

        // Observe elements for animation
        document
            .querySelectorAll(".project-card, .strength-item, .timeline-item")
            .forEach((el) => {
                observer.observe(el);
        });

        // ========================================
        // Activity Heat Map - Real GitHub Data
        // ========================================
        const GITHUB_USERNAME = "Gunnarguy";
        const REPOS = [
            "LinkedOut",
            "OpenResponses",
            "OpenIntelligence",
            "PlaudBlender",
            "OpenCone",
            "OpenAssistant",
        ];

        // ========================================
        // Shared GitHub Data Layer
        // ========================================
        let lastFetchTime = null;
        let isLiveData = false;
        let dataSource = ""; // "json" | "api" | "fallback"
        let refreshTimer = null;
        let rateLimitRemaining = 60;
        // Cache: { repoName: { repoInfo, commits[] } }
        const repoDataCache = {};

        // Load pre-generated stats from GitHub Actions (zero API calls)
        async function loadStaticStats() {
            try {
                const resp = await fetch("data/github-stats.json");
                if (!resp.ok) return false;
                const data = await resp.json();

            for (const [repo, info] of Object.entries(data.repos)) {
                repoDataCache[repo] = {
                    repoInfo: { created_at: info.created_at },
                    commits: info.commits.map((c) => ({
                        sha: c.sha,
                        commit: {
                            message: c.message,
                            author: { date: c.date, name: c.author },
                        },
                    })),
                };
            }

            lastFetchTime = new Date(data.generated);
            dataSource = "json";
            isLiveData = true;
            return true;
        } catch (e) {
            return false;
        }
      }

        // Rate-limit-aware fetch wrapper for live API
        async function ghFetch(url) {
            if (rateLimitRemaining <= 2) return null;
            const response = await fetch(url, {
                headers: { Accept: "application/vnd.github.v3+json" },
            });
            const remaining = response.headers.get("X-RateLimit-Remaining");
            if (remaining !== null) rateLimitRemaining = parseInt(remaining, 10);
            if (!response.ok) return null;
            return response;
        }

        // Live API fetch (used when JSON is stale or missing)
        async function fetchAllRepoData() {
            let anySuccess = false;

          for (const repo of REPOS) {
              try {
                  const infoResp = await ghFetch(
                      `https://api.github.com/repos/${GITHUB_USERNAME}/${repo}`,
                  );
                  let repoInfo = null;
                  if (infoResp) repoInfo = await infoResp.json();

              let allCommits = [];
              let page = 1;
              let hasMore = true;

              while (hasMore && page <= 10) {
                  const resp = await ghFetch(
                      `https://api.github.com/repos/${GITHUB_USERNAME}/${repo}/commits?per_page=100&page=${page}`,
                  );
                  if (!resp) break;
                  const commits = await resp.json();
                  if (commits.length === 0) break;
                  allCommits = allCommits.concat(commits);
                  if (commits.length < 100) hasMore = false;
                  page++;
              }

              if (allCommits.length > 0 || repoInfo) {
                  repoDataCache[repo] = { repoInfo, commits: allCommits };
                  anySuccess = true;
              }
          } catch (error) {
              // Silently skip failed repos
          }
        }

          if (anySuccess) {
              dataSource = "api";
              lastFetchTime = new Date();
          }
          return anySuccess;
      }

        // Build heatmap data from shared cache (all-time)
        function buildHeatmapFromCache() {
        const activityMap = new Map();
        const today = new Date();

          // Find the earliest commit across all repos
          let earliest = today;
          for (const repo of REPOS) {
              const cached = repoDataCache[repo];
              if (!cached) continue;
              cached.commits.forEach((commit) => {
                  const d = new Date(commit.commit.author.date);
                  if (d < earliest) earliest = d;
              });
          }

          // Snap to the Sunday of that week
          const start = new Date(earliest);
          start.setDate(start.getDate() - start.getDay());
          start.setHours(0, 0, 0, 0);

          // Fill every day from start to today
          const totalDays =
              Math.ceil((today - start) / (1000 * 60 * 60 * 24)) + 1;
          for (let i = 0; i < totalDays; i++) {
              const date = new Date(start);
              date.setDate(date.getDate() + i);
              const dateKey = date.toISOString().split("T")[0];
              activityMap.set(dateKey, { date: new Date(date), count: 0 });
        }

          // Tally commits into the map
        for (const repo of REPOS) {
            const cached = repoDataCache[repo];
            if (!cached) continue;
            cached.commits.forEach((commit) => {
                const dateKey = new Date(commit.commit.author.date)
                    .toISOString()
                    .split("T")[0];
                if (activityMap.has(dateKey)) {
                    activityMap.get(dateKey).count++;
                }
          });
        }

        return Array.from(activityMap.values()).sort((a, b) => a.date - b.date);
      }

        // Deterministic fallback data using KNOWN_REPO_DATA aggregates
        function generateFallbackData() {
        const data = [];
        const today = new Date();

          // Deterministic hash (same as tree ring fallback)
          const hash = (str, seed) => {
              let h = seed;
              for (let i = 0; i < str.length; i++) {
                  h = (h << 5) - h + str.charCodeAt(i);
                  h = h & h;
              }
              return Math.abs(h);
          };

          // Distribute known total commits across the year deterministically
          const totalKnown = Object.values(KNOWN_REPO_DATA).reduce(
              (sum, r) => sum + r.totalCommits,
              0,
          );

        for (let i = 364; i >= 0; i--) {
            const date = new Date(today);
            date.setDate(date.getDate() - i);
            const dateKey = date.toISOString().split("T")[0];

            // Hash date string for deterministic activity
            const h = hash(dateKey, 42);
            const isWeekend = date.getDay() === 0 || date.getDay() === 6;
            let count = 0;

            const roll = h % 100;
            if (isWeekend) {
                if (roll > 70) count = (h % 3) + 1;
          } else {
              if (roll > 30) count = 1;
              if (roll > 50) count = (h % 3) + 2;
              if (roll > 80) count = (h % 5) + 5;
              if (roll > 95) count = (h % 8) + 10;
          }

            data.push({ date, count });
        }
        return data;
      }

        function getActivityLevel(count) {
        if (count === 0) return 0;
        if (count <= 2) return 1;
        if (count <= 5) return 2;
        if (count <= 10) return 3;
        return 4;
      }

        async function renderHeatMap() {
            const grid = document.getElementById("heatmap-grid");
            const monthsContainer = document.getElementById("heatmap-months");
            const statsContainer = document.getElementById("heatmap-stats");

        if (!grid) return;

          // Build from cache (already fetched by initAllData)
          let activityData = buildHeatmapFromCache();
          const totalCommits = activityData.reduce((sum, d) => sum + d.count, 0);

          if (totalCommits === 0) {
              activityData = generateFallbackData();
        }

        // Clear existing content
          grid.innerHTML = "";
          monthsContainer.innerHTML = "";

        // Calculate starting position (find first Sunday)
        const firstDate = activityData[0].date;
        const startDay = firstDate.getDay();

        // Create grid with 53 columns (weeks) x 7 rows (days)
        const weeks = [];
        let currentWeek = [];

        // Add empty cells for days before data starts
        for (let i = 0; i < startDay; i++) {
            currentWeek.push(null);
        }

        activityData.forEach((item, index) => {
            currentWeek.push(item);
            if (currentWeek.length === 7) {
                weeks.push(currentWeek);
                currentWeek = [];
            }
        });

        // Add remaining days in last week
        if (currentWeek.length > 0) {
            weeks.push(currentWeek);
        }

        // Render grid
        weeks.forEach((week, weekIndex) => {
            const weekColumn = document.createElement("div");
            weekColumn.className = "heatmap-week";

            week.forEach((day, dayIndex) => {
                const cell = document.createElement("div");
                cell.className = "heatmap-cell";

              if (day) {
                  const level = getActivityLevel(day.count);
                  cell.setAttribute("data-level", level);
                  cell.setAttribute(
                      "data-date",
                      day.date.toLocaleDateString("en-US", {
                          weekday: "short",
                          month: "short",
                          day: "numeric",
                          year: "numeric",
                      }),
                  );
                  cell.setAttribute("data-count", day.count);

                // Tooltip on hover
                cell.title = `${day.count} commits on ${day.date.toLocaleDateString(
                    "en-US",
                    {
                        month: "short",
                        day: "numeric",
                        year: "numeric",
                    },
                )}`;
            } else {
                cell.style.visibility = "hidden";
            }

              weekColumn.appendChild(cell);
          });

            grid.appendChild(weekColumn);
        });

          // Render month + year labels
          const monthNames = [
              "Jan",
              "Feb",
              "Mar",
              "Apr",
              "May",
              "Jun",
              "Jul",
              "Aug",
              "Sep",
              "Oct",
              "Nov",
              "Dec",
          ];
        let lastMonth = -1;
          let lastYear = -1;

        weeks.forEach((week, weekIndex) => {
            const firstValidDay = week.find((d) => d !== null);
            if (firstValidDay) {
                const month = firstValidDay.date.getMonth();
                const year = firstValidDay.date.getFullYear();
                if (month !== lastMonth) {
                    const monthLabel = document.createElement("span");
                    // Show year on January or first label
                    monthLabel.textContent =
                        month === 0 || lastMonth === -1
                            ? `${monthNames[month]} '${String(year).slice(2)}`
                            : monthNames[month];
                    monthLabel.style.left = `${weekIndex * 14 + 28}px`;
                    if (month === 0 && lastYear !== -1)
                        monthLabel.classList.add("year-start");
                    monthsContainer.appendChild(monthLabel);
                    lastMonth = month;
                    lastYear = year;
            }
          }
        });

          // Auto-scroll to present (right edge)
          const wrapper = document.querySelector(".heatmap-container");
          if (wrapper) wrapper.scrollLeft = wrapper.scrollWidth;

        // Calculate stats
          const totalContributions = activityData.reduce(
              (sum, d) => sum + d.count,
              0,
          );
          const totalDaysSpan = activityData.length;

          // Last-year subset
          const oneYearAgo = new Date();
          oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
          const lastYearCommits = activityData
              .filter((d) => d.date >= oneYearAgo)
              .reduce((sum, d) => sum + d.count, 0);

        // Current streak
        let currentStreak = 0;
        for (let i = activityData.length - 1; i >= 0; i--) {
            if (activityData[i].count > 0) {
                currentStreak++;
            } else if (i < activityData.length - 1) {
                break;
            }
        }

        // Longest streak
        let longestStreak = 0;
        let tempStreak = 0;
          activityData.forEach((d) => {
              if (d.count > 0) {
                  tempStreak++;
                  longestStreak = Math.max(longestStreak, tempStreak);
              } else {
                  tempStreak = 0;
              }
        });

        statsContainer.innerHTML = `
                <div class="heatmap-stat">
                    <span class="stat-value">${totalContributions}</span>
                    <span class="stat-label">all-time commits</span>
                </div>
                <div class="heatmap-stat">
                    <span class="stat-value">${lastYearCommits}</span>
                    <span class="stat-label">in the last year</span>
                </div>
                <div class="heatmap-stat">
                    <span class="stat-value">${currentStreak}</span>
                    <span class="stat-label">day current streak</span>
                </div>
                <div class="heatmap-stat">
                    <span class="stat-value">${longestStreak}</span>
                    <span class="stat-label">day longest streak</span>
                </div>
                <div class="heatmap-stat">
                    <span class="stat-value">${(totalContributions / totalDaysSpan).toFixed(1)}</span>
                    <span class="stat-label">average per day</span>
                </div>
            `;
      }

        // Data freshness UI
        function updateDataStatus() {
            const statusDot = document.getElementById("status-dot");
            const statusText = document.getElementById("status-text");
            const refreshBtn = document.getElementById("refresh-btn");

          if (!statusDot || !statusText) return;
          if (refreshBtn) refreshBtn.classList.remove("spinning");

          if (isLiveData && lastFetchTime) {
              statusDot.className = "status-dot live";
              // Show how fresh the data is
              const age = Date.now() - lastFetchTime.getTime();
              const mins = Math.floor(age / 60000);
              const hours = Math.floor(mins / 60);
              let freshness;
              if (mins < 2) freshness = "just now";
              else if (mins < 60) freshness = `${mins}m ago`;
              else if (hours < 24) freshness = `${hours}h ago`;
              else freshness = lastFetchTime.toLocaleDateString();

            const sourceLabel = dataSource === "json" ? "Synced" : "Live";
            statusText.textContent = `${sourceLabel} \u00b7 ${freshness}`;
            statusText.title =
                dataSource === "json"
                    ? `Data from GitHub Actions, generated ${lastFetchTime.toLocaleString()}`
                    : `Live API fetch, rate limit: ${rateLimitRemaining}/60`;
        } else {
            statusDot.className = "status-dot fallback";
            statusText.textContent = "Offline \u00b7 using estimates";
            statusText.title = "Could not reach GitHub. Showing estimated data.";
        }
      }

        // Master init: try static JSON first, then live API, then fallback
        async function initAllData() {
            const statusDot = document.getElementById("status-dot");
            const statusText = document.getElementById("status-text");
            const refreshBtn = document.getElementById("refresh-btn");
            if (statusDot) statusDot.className = "status-dot loading";
            if (statusText) statusText.textContent = "Loading...";
            if (refreshBtn) refreshBtn.classList.add("spinning");

          // Step 1: Try pre-built JSON from GitHub Actions (instant, no rate limit)
          const jsonOk = await loadStaticStats();

          if (!jsonOk) {
              // Step 2: No JSON yet — try live API
              const apiOk = await fetchAllRepoData();
              isLiveData = apiOk;
              if (!apiOk) {
                  dataSource = "fallback";
                  lastFetchTime = null;
              }
          }

          updateDataStatus();

          // Render everything from whatever data we got
          await renderHeatMap();
          REPOS.forEach((repo) => renderTreeRingsFromCache(repo));
      }

        // Force live refresh (bypasses JSON, goes straight to API)
        async function forceRefresh() {
            const statusDot = document.getElementById("status-dot");
            const statusText = document.getElementById("status-text");
            const refreshBtn = document.getElementById("refresh-btn");
            if (statusDot) statusDot.className = "status-dot loading";
            if (statusText) statusText.textContent = "Fetching live...";
            if (refreshBtn) refreshBtn.classList.add("spinning");

          const apiOk = await fetchAllRepoData();
          isLiveData = apiOk;
          if (!apiOk && !lastFetchTime) dataSource = "fallback";
          updateDataStatus();

          await renderHeatMap();
          REPOS.forEach((repo) => renderTreeRingsFromCache(repo));
      }

        // Manual refresh fetches live from API
        document.getElementById("refresh-btn")?.addEventListener("click", (e) => {
            e.preventDefault();
            forceRefresh();
        });

        // Auto-refresh every 15 minutes (pause when tab hidden)
        refreshTimer = setInterval(
            () => {
                if (!document.hidden) initAllData();
            },
            15 * 60 * 1000,
        );

        // ========================================
        // Git Stratigraphy - Tree Ring Visualization
        // ========================================
        // Note: REPOS and GITHUB_USERNAME are already defined in heatmap section

        // Known repo data (verified by user)
        const KNOWN_REPO_DATA = {
            LinkedOut: {
                created: "2026-03-10",
                startYear: 2026,
                totalCommits: 47,
                weeksActive: 1,
            },
            OpenAssistant: {
                created: "2024-09-20",
                startYear: 2024,
                totalCommits: 214,
                weeksActive: 29,
        },
          OpenCone: {
              created: "2025-04-02",
              startYear: 2025,
              totalCommits: 122,
              weeksActive: 16,
        },
          OpenIntelligence: {
              created: "2025-10-11",
              startYear: 2025,
              totalCommits: 202,
              weeksActive: 20,
        },
          OpenResponses: {
              created: "2025-06-28",
              startYear: 2025,
              totalCommits: 88,
              weeksActive: 17,
          },
          PlaudBlender: {
              created: "2025-12-04",
              startYear: 2025,
              totalCommits: 57,
              weeksActive: 6,
          },
      };

        // Categorize commit by message
        function categorizeCommit(message) {
        const msg = message.toLowerCase();
          if (
              msg.includes("feat") ||
              msg.includes("add") ||
              msg.includes("new") ||
              msg.includes("implement")
          ) {
              return "feat";
          } else if (
              msg.includes("fix") ||
              msg.includes("bug") ||
              msg.includes("patch") ||
              msg.includes("hotfix")
          ) {
              return "fix";
          } else if (
              msg.includes("refactor") ||
              msg.includes("clean") ||
              msg.includes("restructure") ||
              msg.includes("optimize")
          ) {
              return "refactor";
        } else {
            return "docs";
        }
      }

        // Group commits by week so the final rings stay in chronological order
        function groupByWeek(commits) {
        const weeks = new Map();

          commits.forEach((commit) => {
              const date = new Date(commit.date);
              // Get Monday of that week
              const day = date.getDay();
              const diff = date.getDate() - day + (day === 0 ? -6 : 1);
              const monday = new Date(date.setDate(diff));
              const weekKey = monday.toISOString().split("T")[0];

            if (!weeks.has(weekKey)) {
                weeks.set(weekKey, {
                    weekStart: weekKey,
                    commits: [],
                    types: { feat: 0, fix: 0, refactor: 0, docs: 0 },
            });
          }

            const week = weeks.get(weekKey);
            week.commits.push(commit);
            week.types[commit.type]++;
        });

        // Sort by date ascending (oldest first = center of tree)
          return Array.from(weeks.values()).sort(
              (a, b) => new Date(a.weekStart) - new Date(b.weekStart),
        );
      }

        // Fallback type if a commit is missing its own classification
        function getDominantType(types) {
        let max = 0;
          let dominant = "docs";
        for (const [type, count] of Object.entries(types)) {
            if (count > max) {
                max = count;
                dominant = type;
            }
        }
        return dominant;
      }

        // Generate SVG tree rings
        function generateTreeRings(
            svg,
            weeklyData,
            repoName,
            startYear,
            totalCommits,
        ) {
        const size = 300;
        const center = size / 2;
        const coreRadius = 12;
        const maxRadius = 138;

          // Flatten weekly buckets back into a chronological per-commit list
        const allCommits = [];
          weeklyData.forEach((week) => {
              week.commits.forEach((commit) => {
                  allCommits.push({
                      type: commit.type || getDominantType(week.types),
                      message: commit.message,
                      weekStart: week.weekStart,
            });
          });
        });

        // 1 COMMIT = 1 RING - use actual commit count from data
        const numRings = allCommits.length || totalCommits || 1;

        // Ring spacing - all trees fill to maxRadius completely
        const availableSpace = maxRadius - coreRadius;
        const RING_SPACING = availableSpace / numRings;

        // Stroke width matches spacing so rings touch (no gaps)
        const strokeWidth = RING_SPACING;

        // Clear existing
          svg.innerHTML = "";

        // Add wood grain texture definition
          const defs = document.createElementNS(
              "http://www.w3.org/2000/svg",
              "defs",
          );
        defs.innerHTML = `
            <filter id="grain-${repoName}">
                <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise"/>
                <feDiffuseLighting in="noise" lighting-color="#8b5e34" surfaceScale="1.5">
                    <feDistantLight azimuth="45" elevation="60"/>
                </feDiffuseLighting>
            </filter>
        `;
        svg.appendChild(defs);

        // Background circle - always full size
          const bg = document.createElementNS(
              "http://www.w3.org/2000/svg",
              "circle",
          );
          bg.setAttribute("cx", center);
          bg.setAttribute("cy", center);
          bg.setAttribute("r", maxRadius);
          bg.setAttribute("fill", "#1a0f0a");
        svg.appendChild(bg);

        // Create 1 ring per commit - fills entire circle
        allCommits.forEach((commit, i) => {
            // Position ring so they fill from core to edge
            const radius = coreRadius + (i + 0.5) * RING_SPACING;
            const type = commit.type || "docs";

            const ring = document.createElementNS(
                "http://www.w3.org/2000/svg",
                "circle",
            );
            ring.setAttribute("cx", center);
            ring.setAttribute("cy", center);
            ring.setAttribute("r", radius);
            ring.setAttribute("class", `ring ${type}`);
            ring.setAttribute("stroke-width", strokeWidth);
            ring.setAttribute("stroke-opacity", "1");
            ring.setAttribute("data-commits", "1");
            ring.setAttribute("data-type", type);
            ring.setAttribute("data-messages", commit.message || "");

            svg.appendChild(ring);
        });

        // Core (center of tree)
          const core = document.createElementNS(
              "http://www.w3.org/2000/svg",
              "circle",
          );
          core.setAttribute("cx", center);
          core.setAttribute("cy", center);
          core.setAttribute("r", coreRadius);
          core.setAttribute("class", "core");
        svg.appendChild(core);

        // Core label - show start year
          const text = document.createElementNS(
              "http://www.w3.org/2000/svg",
              "text",
          );
          text.setAttribute("x", center);
          text.setAttribute("y", center);
          text.setAttribute("class", "core-text");
          text.textContent = startYear || "?";
        svg.appendChild(text);
      }

        // Setup tooltip interactions
        function setupTooltip(container) {
            const svg = container.querySelector(".tree-rings");
            const tooltip = container.querySelector(".tree-tooltip");

          svg.addEventListener("mousemove", (e) => {
              const ring = e.target.closest(".ring");
              if (!ring) {
                  tooltip.classList.remove("visible");
                  return;
          }

            const commits = ring.getAttribute("data-commits");
            const type = ring.getAttribute("data-type");
            const messages =
                ring
                    .getAttribute("data-messages")
                    ?.split("|")
                    .filter((m) => m) || [];

            const typeLabel =
                {
                    feat: "Features",
                    fix: "Bug Fixes",
                    refactor: "Refactors",
                    docs: "Docs/Other",
            }[type] || type;

            tooltip.innerHTML = `
                <div class="tooltip-commits">${commits} commit${commits !== "1" ? "s" : ""}</div>
                <div class="tooltip-type" style="color: var(--${type}-color, #fff)">${typeLabel}</div>
                ${messages.length > 0 ? `<div class="tooltip-message">${messages[0].substring(0, 50)}${messages[0].length > 50 ? "..." : ""}</div>` : ""}
            `;

            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            tooltip.style.left = `${x + 15}px`;
            tooltip.style.top = `${y - 10}px`;
            tooltip.classList.add("visible");
        });

          svg.addEventListener("mouseleave", () => {
              tooltip.classList.remove("visible");
        });
      }

        // Render tree rings from shared cache (no extra API calls)
        function renderTreeRingsFromCache(repoName) {
            const container = document.querySelector(
                `.tree-sample[data-repo="${repoName}"]`,
            );
        if (!container) return;

          container.classList.add("loading");

          const svg = container.querySelector(".tree-rings");
          const ageLabel = container.querySelector(".tree-age");
          const stats = container.querySelectorAll(".tree-stat .stat-num");
          const cached = repoDataCache[repoName];

          if (cached && cached.commits.length > 0) {
              // We have real data from the shared fetch
              const repoCreatedAt = cached.repoInfo
                  ? new Date(cached.repoInfo.created_at)
                  : null;

            const processedCommits = cached.commits.map((c) => ({
                sha: c.sha,
                message: c.commit.message.split("\n")[0],
                date: c.commit.author.date,
                author: c.commit.author.name,
                type: categorizeCommit(c.commit.message),
          }));

            const weeklyData = groupByWeek(processedCommits);

            const projectStartDate =
                repoCreatedAt ||
                (processedCommits.length > 0
                    ? new Date(processedCommits[processedCommits.length - 1].date)
                    : new Date());

            // Calculate project age from creation date to now
            const now = new Date();
            const ageMonths = Math.floor(
                (now - projectStartDate) / (1000 * 60 * 60 * 24 * 30),
            );

            if (ageMonths >= 12) {
                const years = Math.floor(ageMonths / 12);
                const months = ageMonths % 12;
                ageLabel.textContent = `${years}y ${months}m old`;
            } else {
                ageLabel.textContent = `${ageMonths}m old`;
            }

            // Update stats
            const uniqueAuthors = new Set(processedCommits.map((c) => c.author))
                .size;
            const totalCommits = processedCommits.length;
            stats[0].textContent = totalCommits;
            stats[1].textContent = weeklyData.length;
            stats[2].textContent = uniqueAuthors;

            // Generate visualization with correct start year
            const startYear = projectStartDate.getFullYear();
            generateTreeRings(svg, weeklyData, repoName, startYear, totalCommits);
            setupTooltip(container);
        } else {
            // No cached data — use known fallback

            // Use hardcoded known data for this repo
            const knownData = KNOWN_REPO_DATA[repoName];
            const types = ["feat", "fix", "refactor", "docs"];
            const createdDate = knownData
                ? new Date(knownData.created)
                : new Date("2024-01-01");
            const totalCommits = knownData ? knownData.totalCommits : 100;

            // Simple hash function for deterministic "random" based on repo name
            const hash = (str, seed) => {
                let h = seed;
                for (let i = 0; i < str.length; i++) {
                    h = (h << 5) - h + str.charCodeAt(i);
                    h = h & h;
                }
                return Math.abs(h);
          };

            // Generate deterministic commits - same every time for this repo
            const demoWeeks = [
                {
                    weekStart: createdDate.toISOString().split("T")[0],
                    commits: Array(totalCommits)
                        .fill(null)
                        .map((_, i) => {
                            // Deterministic type based on repo name + commit index
                            const typeIndex = hash(repoName, i) % 4;
                            return {
                                message: `Commit ${i + 1}`,
                                type: types[typeIndex],
                  };
                }),
                  types: { feat: 0, fix: 0, refactor: 0, docs: 0 },
              },
          ];

            // Calculate accurate age from known creation date
            const now = new Date();
            const ageMonths = Math.floor(
                (now - createdDate) / (1000 * 60 * 60 * 24 * 30),
            );
            if (ageMonths >= 12) {
                const years = Math.floor(ageMonths / 12);
                const months = ageMonths % 12;
                ageLabel.textContent = `${years}y ${months}m old`;
            } else {
                ageLabel.textContent = `${ageMonths}m old`;
            }

            stats[0].textContent = totalCommits;
            stats[1].textContent = knownData ? knownData.weeksActive : 50;
            stats[2].textContent = "1";

            // Use known start year
            const startYear = knownData ? knownData.startYear : 2024;
            generateTreeRings(svg, demoWeeks, repoName, startYear, totalCommits);
            setupTooltip(container);
        }

          container.classList.remove("loading");
      }

        // Initialize everything — single shared fetch
        initAllData();
    </script>
