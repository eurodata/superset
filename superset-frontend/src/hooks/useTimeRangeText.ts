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

import { useEffect, useState } from 'react';
import {
  DataMaskStateWithId,
  DataMaskWithId,
  fetchTimeRange,
} from '@superset-ui/core';
import { RootState } from 'src/dashboard/types';
import { useSelector } from 'react-redux';
import getBootstrapData from 'src/utils/getBootstrapData';

const formatTimeRangeText = (range = '') => {
  const regex = /(\d{4}-\d{2}-\d{2}) ≤ col < (\d{4}-\d{2}-\d{2})/;
  const match = range.match(regex);
  if (!match) return '';
  const [, start, end] = match;

  const startDate = new Date(start);
  const endDate = new Date(end);
  endDate.setDate(endDate.getDate() - 1);

  const { locale } = getBootstrapData().common;
  return `${startDate.toLocaleDateString(
    locale,
  )} – ${endDate.toLocaleDateString(locale)}`;
};

export function useDashboardTimeRangeText(fallback = 'Last year') {
  const dataMask = useSelector<RootState, DataMaskStateWithId>(s => s.dataMask);
  const [timeRangeText, setTimeRangeText] = useState('');

  useEffect(() => {
    const timeRange = Object.values(dataMask).find(
      (f: DataMaskWithId) => f.extraFormData?.time_range,
    )?.extraFormData?.time_range;

    fetchTimeRange(timeRange ?? fallback).then(({ value }) => {
      setTimeRangeText(formatTimeRangeText(value));
    });
  }, [dataMask, fallback]);

  return timeRangeText;
}

export function useTimeRangeText(defaultTimeRange = 'Last year') {
  const dataMask = useSelector<RootState, DataMaskStateWithId>(s => s.dataMask);
  const [timeRangeText, setTimeRangeText] = useState('');

  useEffect(() => {
    const timeRange = Object.values(dataMask).find(
      (f: DataMaskWithId) => f.extraFormData?.time_range,
    )?.extraFormData?.time_range;

    fetchTimeRange(timeRange ?? defaultTimeRange).then(({ value }) => {
      setTimeRangeText(formatTimeRangeText(value));
    });
  }, [dataMask]);

  return timeRangeText;
}
