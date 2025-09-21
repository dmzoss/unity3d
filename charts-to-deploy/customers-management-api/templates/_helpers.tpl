{{/* Common labels */}}
{{- define "customers-management-api.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/* Common names */}}
{{- define "customers-management-api.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end }}