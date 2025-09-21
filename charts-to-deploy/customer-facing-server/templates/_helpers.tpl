{{/* Common labels */}}
{{- define "customer-facing-server.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/* Common names */}}
{{- define "customer-facing-server.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end }}
