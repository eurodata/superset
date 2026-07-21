/*
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

import { NumberFormatter } from '@superset-ui/core';

export default function createDurationHHMMFormatter(
  config: {
    multiplier?: number;
  } = {},
) {
  const { multiplier = 1 } = config;

  return new NumberFormatter({
    description: 'Duration as HH:MM from milliseconds',
    formatFunc: value => {
      const milliseconds = value * multiplier;
      const totalSeconds = milliseconds / 1000;
      const totalMinutes = Math.round(totalSeconds / 60);
      const hours = Math.floor(totalMinutes / 60);
      const minutes = totalMinutes % 60;

      const hh = String(hours).padStart(2, '0');
      const mm = String(minutes).padStart(2, '0');
      return `${hh}:${mm}`;
    },
    id: 'duration_format_hhmm',
    label: `Duration formatter HHMM`,
  });
}
