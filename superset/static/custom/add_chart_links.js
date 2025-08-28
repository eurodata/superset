/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

const appContainer = document.getElementById('app');
const dataBootstrap = appContainer?.getAttribute('data-bootstrap');
const documentationResolverUrl = JSON.parse(dataBootstrap)?.common?.documentation_resolver?.url;

if (documentationResolverUrl) {
  const observer = new MutationObserver(() => {
    const charts = document.querySelectorAll('[data-test-chart-id]');
    if (charts.length > 0) {
      charts.forEach(chart => {
        if (chart.querySelector('.info-icon')) return;

        const sliceId = chart.getAttribute('data-test-chart-id');
        const headerControls = chart.querySelector('.header-controls');

        const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        icon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
        icon.setAttribute('width', '24');
        icon.setAttribute('height', '24');
        icon.setAttribute('viewBox', '0 0 24 24');
        icon.classList.add('info-icon');
        icon.style.cursor = 'pointer';

        icon.innerHTML = `
          <path xmlns="http://www.w3.org/2000/svg" d="M16,10c0,2.5-3,3.349-3,5H11c0-2.633,3-3,3-5a2,2,0,0,0-4,0H8a4,4,0,0,1,8,0Zm6,2A10,10,0,1,1,12,2,10.0152,10.0152,0,0,1,22,12Zm-2,0a8,8,0,1,0-8,8A7.9849,7.9849,0,0,0,20,12Zm-8,3.75A1.25,1.25,0,1,0,13.25,17,1.25,1.25,0,0,0,12,15.75Z"/>
        `;

        icon.addEventListener('click', () => {
          const link = `${documentationResolverUrl}${sliceId}`;
          window.open(link, '_blank');
        });

        headerControls.insertBefore(icon, headerControls.firstChild);
      });
    }
  });

  // Start observing
  observer.observe(document.body, { childList: true, subtree: true });
}
