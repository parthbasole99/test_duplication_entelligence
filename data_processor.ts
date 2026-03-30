/**
 * Data Processing Service (TypeScript version)
 *
 * This file mirrors the Python data_processor.py patterns
 * to test cross-language EKU matching.
 *
 * Some patterns ARE valid issues in TS, some are FALSE POSITIVES
 * because TypeScript has different idioms (optional chaining, type guards, etc.)
 */

import axios from 'axios';

// --- SHOULD BE FALSE POSITIVE: TypeScript optional chaining handles this ---
interface UserProfile {
  display_name?: string;
  contact?: { email?: string };
  subscription?: { tier?: string };
  organization?: { id?: string };
}

async function syncUserProfile(userId: string, apiToken: string): Promise<Record<string, string>> {
  const response = await axios.get<UserProfile>(
    `https://api.accounts.com/users/${userId}`,
    { headers: { Authorization: `Bearer ${apiToken}` }, timeout: 30000 }
  );
  const profile = response.data;
  // Using optional chaining — NOT the same as Python's profile["display_name"]
  return {
    name: profile.display_name ?? 'Unknown',
    email: profile.contact?.email ?? '',
    tier: profile.subscription?.tier ?? 'free',
    orgId: profile.organization?.id ?? '',
  };
}


// --- SHOULD BE TRUE POSITIVE: unguarded array access, same risk as Python ---
interface DeploymentResponse {
  deployments: Array<{ id: string; commits: Array<{ sha: string }> }>;
}

async function fetchLatestDeployment(apiUrl: string, token: string): Promise<Record<string, string>> {
  const response = await axios.get<DeploymentResponse>(
    `${apiUrl}/deployments`,
    { headers: { Authorization: `Bearer ${token}` }, timeout: 30000 }
  );
  const data = response.data;
  const latest = data.deployments[0];  // Can throw if deployments is empty
  const commit = latest.commits[0].sha; // Nested unguarded access
  return { deploymentId: latest.id, commit };
}


// --- SHOULD BE FALSE POSITIVE: TypeScript type system prevents this ---
interface AlertConfig {
  severity: string;
  threshold: number;
  channelId: string;
}

function createAlert(severity: string, threshold: number, channelId: string): Record<string, unknown> {
  return { severity, threshold, channel_id: channelId };
}

function setupMonitoring(config: AlertConfig) {
  // TypeScript compiler catches type mismatches — parameter_position_mismatch is a Python issue
  return createAlert(config.severity, config.threshold, config.channelId);
}


// --- SHOULD BE TRUE POSITIVE: unguarded dict access, same as Python ---
function getUserPermissions(config: Record<string, any>, userId: string): string[] {
  const role = config['roles'][userId];               // Can throw if userId missing
  const permissions = config['permissions'][role];     // Can throw if role not in permissions
  const org = config['org_settings']['default_org'];   // Unguarded nested access
  return permissions;
}


// --- SHOULD BE FALSE POSITIVE: proper error handling with try-catch ---
async function ingestPartnerFeed(feedUrl: string): Promise<Array<Record<string, string>>> {
  const response = await axios.get(feedUrl, { timeout: 60000 });
  const feed = response.data;
  const items: Array<Record<string, string>> = [];

  try {
    for (const entry of feed.results) {
      items.push({
        sku: entry.product.sku,
        price: entry.pricing.amount,
        currency: entry.pricing.currency,
        warehouse: entry.fulfillment.warehouse_id,
      });
    }
  } catch (error) {
    console.error('Failed to parse partner feed entry:', error);
  }

  return items;
}


// --- SHOULD BE TRUE POSITIVE: unguarded webhook parsing, same risk ---
interface WebhookPayload {
  body?: string;
}

function parseEventBody(body: string): Record<string, any> {
  return body ? JSON.parse(body) : {};
}

function processWebhookEvent(eventPayload: WebhookPayload): Record<string, string> {
  const parsed = parseEventBody(eventPayload.body ?? '');
  const eventType = parsed['type'];          // Can be undefined
  const entityId = parsed['data']['id'];     // Can throw if data is undefined
  const actions = parsed['actions'];
  const firstAction = actions[0]['name'];    // Can throw if actions is empty
  return { eventType, entityId, action: firstAction };
}


// --- Division by zero — same issue as Python ---
function totalCalcs(items: number[]): number {
  const total = items.reduce((sum, item) => sum + item, 0);
  const average = total / items.length;  // NaN if empty (not exception like Python, but still a bug)
  return average;
}

export {
  syncUserProfile,
  fetchLatestDeployment,
  setupMonitoring,
  getUserPermissions,
  ingestPartnerFeed,
  processWebhookEvent,
  totalCalcs,
};
